#!/usr/bin/env python

# Copyright (C) 2019 by eHealth Africa : http://www.eHealthAfrica.org
#
# See the NOTICE file distributed with this work for additional information
# regarding copyright ownership.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from datetime import datetime
import json
from uuid import UUID
import os
import logging
import time
import threading
import redis
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    NamedTuple,
    Union
)

DEFAULT_TENANT = os.environ.get('DEFAULT_REALM', 'no-tenant')
LOG = logging.getLogger(__name__)
LOG.setLevel(os.environ.get('LOGGING_LEVEL', 'ERROR'))

KEEP_ALIVE_INTERVAL = 10


def get_settings(setting):
    if isinstance(setting, tuple):
        return setting[0]
    try:
        return setting
    except AttributeError:
        return None


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)  # pragma: no cover


class Task(NamedTuple):
    id: str
    tenant: str
    type: str                # object type in redis
    data: Union[Dict, None]  # the message value from redis


class TaskEvent(NamedTuple):
    task_id: str    # event pertains to this task
    tenant: str
    type: str       # object type in redis
    event: str      # event type in redis (set, del, etc)


class TaskHelper(object):

    def __init__(self, settings, redis_instance=None):
        self.redis_db = get_settings(settings.REDIS_DB)
        if redis_instance:
            self.redis = redis_instance
        else:
            self.redis = redis.Redis(
                host=get_settings(settings.REDIS_HOST),
                port=get_settings(settings.REDIS_PORT),
                password=get_settings(settings.REDIS_PASSWORD),
                db=self.redis_db,
                encoding='utf-8',
                decode_responses=True,
            )

        self.pubsub = None
        self._subscribe_thread = None
        self.keep_alive = False
        self.keep_alive_thread = None

    # Generic Redis Task Functions
    def add(
        self,
        task: Dict[str, Any],
        type: str,
        tenant: str
    ) -> bool:
        _id = task['id']
        key = f'_{type}:{tenant}:{_id}'
        task['modified'] = datetime.now().isoformat()
        res = self.redis.set(key, json.dumps(task, cls=UUIDEncoder))
        self.notify(tenant, 'set', type, _id)
        return res

    def exists(
        self,
        _id: str,
        type: str,
        tenant: str
    ) -> bool:
        task_id = f'_{type}:{tenant}:{_id}'
        if self.redis.exists(task_id):
            return True
        return False

    def remove(
        self,
        _id: str,
        type: str,
        tenant: str
    ) -> bool:
        task_id = f'_{type}:{tenant}:{_id}'
        res = self.redis.delete(task_id)
        if not res:
            return False
        self.notify(tenant, 'del', type, _id)
        return True

    def get(
        self,
        _id: str,
        type: str,
        tenant: str
    ) -> Dict:
        task_id = f'_{type}:{tenant}:{_id}'
        return self.get_by_key(task_id)

    def get_by_key(self, key: str):
        task = self.redis.get(key)
        if not task:
            raise ValueError(f'No task with id {key}')
        return json.loads(task)

    def list(
        self,
        _type: str,
        tenant: str = None  # No tenants is _all_ tenants
    ) -> Iterable[str]:
        # ids of matching assets as a generator
        if '*' in _type:
            raise ValueError('Type may not include a * wild card.')
        if tenant:
            if '*' in tenant:
                raise ValueError('Tenant may not include a * wild card.')
            key_identifier = f'_{_type}:{tenant}:*'
        else:
            key_identifier = f'_{_type}:*'
        for i in self.redis.scan_iter(key_identifier):
            if not isinstance(i, str):
                i = i.decode('utf-8')
            p = i.split(key_identifier[:-1])
            yield p[1]

    # subscription tasks

    def subscribe(self, callback: Callable, pattern: str, keep_alive: bool):
        self.keep_alive = keep_alive
        if not self._subscribe_thread or not self._subscribe_thread._running:
            self._init_subscriber(callback, pattern)
        else:
            self._subscribe(callback, pattern)

        if self.keep_alive:
            self.keep_alive_thread = threading.Thread(
                target=self.keep_alive_monitor,
                args=(callback, pattern)
            )
            self.keep_alive_thread.start()

    def keep_alive_monitor(self, callback, pattern):
        current_status = False
        pervious_status = True
        while self.keep_alive:
            try:
                # don't ping the pubsub redis, it only handles sub/unsub
                self.redis.ping()
                current_status = True
            except Exception:   # pragma: no cover
                current_status = False
                LOG.debug('Redis server is down.')
            if not pervious_status and current_status:  # pragma: no cover
                LOG.debug('Restarting...')
                self._init_subscriber(callback, pattern)
            pervious_status = current_status
            time.sleep(KEEP_ALIVE_INTERVAL)

    def _init_subscriber(self, callback: Callable, pattern: str):
        LOG.debug('Initializing Redis subscriber')
        self.pubsub = self.redis.pubsub()
        self._subscribe(callback, pattern)
        self._subscribe_thread = self.pubsub.run_in_thread(sleep_time=0.1)
        LOG.debug('Subscriber Running')

    def _subscribe(self, callback: Callable, pattern: str):
        LOG.debug(f'Subscribing to {pattern}')
        keyspace = f'eventspace_{self.redis_db}__:{pattern}'
        self.pubsub.psubscribe(**{
            f'{keyspace}': self._subscriber_wrapper(callback, keyspace)
        })
        LOG.debug(f'Added {keyspace}')

    def _subscriber_wrapper(
        self,
        fn: Callable,
        registered_channel: str
    ) -> Callable:
        # wraps the callback function so that on create/ update,
        # the message instead of the event will be returned
        def wrapper(msg) -> None:
            LOG.debug(f'callback got message: {msg}')
            channel = msg['channel']
            # get _id, tenant from channel: __keyspace@0__:_test:_tenant:00001
            # where id = 00001
            channel = channel if isinstance(channel, str) else channel.decode()
            keyspace, _type, tenant, _id = channel.split(':')
            redis_data = msg['data'] if isinstance(msg['data'], str) else msg['data'].decode()
            LOG.debug(f'Channel: {channel} received {redis_data};'
                      + f' registered on: {registered_channel}')
            res = None
            if redis_data == 'set':    # pragma: no cover
                key = ':'.join([_type, tenant, _id])
                message = self.redis.get(key)
                res = Task(
                    id=_id,
                    tenant=tenant,
                    type=_type,
                    data=json.loads(message)
                )
                LOG.debug(f'ID: {_id} data: {message}')
            else:
                res = TaskEvent(
                    task_id=_id,
                    tenant=tenant,
                    type=_type,
                    event=redis_data
                )
                LOG.debug(f'ID: {_id} event: {redis_data}')
            fn(res)  # On callback, hit registered function with proper data
        return wrapper

    def notify(self, tenant, operation, type, _id):
        key = f'_{type}:{tenant}:{_id}'
        channel = f'eventspace_{self.redis_db}__:{key}'
        LOG.debug(f'Notify {channel} of {operation}')
        return self.redis.publish(channel, operation)

    def publish(
        self,
        task: Dict[str, Any],
        type: str,
        tenant: str
    ):
        _id = task['id']
        key = f'_{type}:{tenant}:{_id}'
        channel = f'eventspace_{self.redis_db}__:{key}'
        LOG.debug(f'Published to {channel}')
        return self.redis.publish(channel, json.dumps(task, cls=UUIDEncoder))

    def get_keys(self, pattern: str):
        return self.redis.execute_command('keys', pattern)

    def _unsubscribe_all(self) -> None:
        LOG.debug('Unsubscribing from all pub-sub topics')
        self.pubsub.punsubscribe()

    def stop(self, *args, **kwargs) -> None:
        self._unsubscribe_all()
        if self._subscribe_thread and self._subscribe_thread._running:  # pragma: no cover
            LOG.debug('Stopping Subscriber thread.')
            try:
                self._subscribe_thread.stop()
            except (
                redis.exceptions.ConnectionError,
                AttributeError
            ):  # pragma: no cover
                LOG.error('Could not explicitly stop subscribe thread: no connection')

        self.keep_alive = False
