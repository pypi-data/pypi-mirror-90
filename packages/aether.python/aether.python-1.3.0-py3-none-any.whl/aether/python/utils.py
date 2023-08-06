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

import requests
from time import sleep
from aether.python.constants import MergeOptions as MERGE_OPTIONS


def object_contains(test, obj):
    # Recursive object comparison function.
    if obj == test:
        return True
    if isinstance(obj, list):
        return True in [object_contains(test, i) for i in obj]
    elif isinstance(obj, dict):
        return True in [object_contains(test, i) for i in obj.values()]
    return False


def merge_objects(source, target, direction):
    # Merge 2 objects
    #
    # Default merge operation is prefer_new
    # Params <source='Original object'>, <target='New object'>,
    # <direction='Direction of merge, determins primacy:
    # use constants.MergeOptions.[prefer_new, prefer_existing]'>
    # # direction Options:
    # prefer_new > (Target to Source) Target takes primacy,
    # prefer_existing > (Source to Target) Source takes primacy
    result = {}
    if direction == MERGE_OPTIONS.fww.value:
        for key in source:
            target[key] = source[key]
        result = target
    elif direction == MERGE_OPTIONS.lww.value:
        for key in target:
            source[key] = target[key]
        result = source
    else:
        result = target
    return result


def replace_nested(_dict, keys, value, replace_missing=True):
    '''
    Puts a value into an existing structure.

    _dict = {"a": {"b": []}}
    keys = ["a", "b"]
    value = 2
    {"a": {"b": 2}} = replace_nested(_dict, keys, value)
    keys = ["a", "c"]
    # replace_missing flag allows for creation of new keys in place.
    {"a": {"b": 2}, "c": 2} = replace_nested(_dict, keys, value, replace_missing=True)

    '''
    if len(keys) == 0:
        raise ValueError('You must specify a path to replace')
    elif len(keys) > 1:
        try:
            _dict[keys[0]] = replace_nested(
                _dict[keys[0]],
                keys[1:],
                value,
                replace_missing
            )
        except KeyError as ker:
            if not replace_missing:
                raise ker
            _dict[keys[0]] = {}
            _dict[keys[0]] = replace_nested(
                _dict[keys[0]],
                keys[1:],
                value,
                replace_missing
            )
    else:
        _dict[keys[0]] = value
    return _dict


def request(*args, **kwargs):
    '''
    Executes the request call at least three times to avoid
    unexpected connection errors (not request expected ones).
    Like:
        # ConnectionResetError: [Errno 104] Connection reset by peer
        # http.client.RemoteDisconnected: Remote end closed connection without response
    '''

    count = 0
    exception = None

    while count < 3:
        try:
            return requests.request(*args, **kwargs)
        except Exception as e:
            exception = e
        count += 1
        sleep(1)

    raise exception
