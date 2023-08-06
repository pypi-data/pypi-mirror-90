# Copyright (C) 2019 by eHealth Africa : http://www.eHealthAfrica.org
#
# See the NOTICE file distributed with this work for additional information
# regarding copyright ownership.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
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

from copy import copy
import json
from typing import Any, List, Mapping, Union


class Node:
    '''
    Helps operationalize avro schemas, particularly with @aether annotations.
    '''

    fields = [
        'doc',
        'name',
        'namespace',
        'default',
        '__default_visualization',  # @aether__ - > __
        '__extended_type',  # @aether__ - > __
        '__lookup'  # @aether__ - > __
    ]

    # fields we have to derive from the original
    calculated_fields = [
        'avro_type',
        'logical_type',
        'optional'
    ]

    # standard Avro attributes
    default: str
    doc: str
    name: str
    namespace: str
    type: Union[str, List[Any]]
    # @aether fields
    __extended_type: str
    __lookup: List[Mapping[str, str]]
    # utility
    _source: str  # source Avro as json string
    has_children: bool
    # heirarchy
    children: Mapping[str, Any]

    def __init__(self, source: Mapping[Any, Any], optional=False):
        self._source = json.dumps(source, sort_keys=True)
        self.has_children = False
        self.children = {}
        self.parse(source)
        self.parse_children(source)

    # Node comparison methods
    @staticmethod
    def compare(left, right):
        paths = left.iter_children()
        differences = {}
        for p in paths:
            diff = []
            try:
                l_node = left.get_node(p)
                r_node = right.get_node(p)
            except ValueError:
                diff = copy(Node.fields)
            else:
                diff = Node.diff_nodes(l_node, r_node)
            if diff:
                differences[p] = diff
        return differences

    @staticmethod
    def diff_nodes(left, right):
        return [f for f in (Node.fields + Node.calculated_fields)
                if not Node.compare_objects(
                    getattr(left, f, None),
                    getattr(right, f, None)
        )]

    @staticmethod
    def compare_objects(a, b):
        try:
            a = json.dumps(a, sort_keys=True)
            b = json.dumps(b, sort_keys=True)
            return a == b
        except Exception:
            return a == b

    def __swap_name(self, name):
        ''' we can't have python attributes that start with @aether
            so we make a simple substitution
        '''
        if name.startswith('__'):
            return f'@aether_{name.lstrip("__")}'
        return name

    def _get_avro_type(self, _type):
        ''' parse the avro types of this node'''
        if isinstance(_type, str):
            yield _type
        elif isinstance(_type, list):
            for i in _type:
                yield from self._get_avro_type(i)
        elif isinstance(_type, dict):
            if '@aether_extended_type' in _type:
                yield _type['@aether_extended_type']
            if 'logicalType' in _type:
                setattr(self, 'logical_type', _type['logicalType'])
                yield _type['type']
            elif 'name' in _type:
                yield f'object:{_type["name"]}'
            elif 'items' in _type:
                yield f'array:{_type["items"]}'
            else:
                yield 'object'

    def parse(self, source: Mapping[Any, Any]):
        fields = {f: self.__swap_name(f) for f in Node.fields}
        for field, alias in fields.items():
            if source.get(alias):
                setattr(self, field, source.get(alias))

        __types = [i for i in self._get_avro_type(source.get('type'))]
        if 'logicalType' in source:
            setattr(self, 'logical_type', source['logicalType'])
        setattr(self, 'avro_type', __types)
        setattr(self, 'optional', ('null' in __types))

    def __is_array(self, field):
        for i in field.get('type', []):
            if isinstance(i, dict):
                if i.get('type') == 'array':
                    return True
        return False

    def parse_children(self, source: Mapping[Any, Any]):
        # node is a mandatory record containing sub-fields
        if isinstance(source.get('type'), dict):
            self.parse_children(source.get('type'))
        fields = source.get('fields', [])
        for f in fields:
            self.has_children = True
            name = f.get('name')
            if self.__is_array(f):
                self.children[name] = Node(f)
                continue
            grand_children = [i for i in f.get('type', []) if isinstance(i, dict)]
            if not grand_children:
                if not name:  # array values, ignore them
                    continue
                self.children[name] = Node(f)
            else:
                for gc in grand_children:
                    name = gc.get('name')
                    _logical_type = gc.get('logicalType')
                    if _logical_type:
                        self.children[f.get('name')] = Node(f)
                    if not name:  # array values, ignore them
                        continue
                    self.children[name] = Node(gc)

    def iter_children(self, parent=''):
        lineage = f'{parent}.{self.name}' if parent else self.name
        if not self.has_children:
            yield lineage
        else:
            for key, child in self.children.items():
                for i in child.iter_children(lineage):
                    yield i

    def test_node(self, conditions):
        # test node for ANY in [has_attr, match_attr, attr_contains]
        for attr in conditions.get('has_attr', []):
            if getattr(self, attr, None):
                return True
        for condition in conditions.get('match_attr', []):
            for k, v in condition.items():
                if getattr(self, k, None) == v:
                    return True
        for condition in conditions.get('attr_contains', []):
            for k, v in condition.items():
                if v in getattr(self, k, []):
                    return True
        return False

    def find_children(self, conditions, parent=''):
        lineage = f'{parent}.{self.name}' if parent else self.name
        if self.test_node(conditions):
            yield lineage
        if self.has_children:
            for child in self.children.values():
                for i in child.find_children(conditions, parent=lineage):
                    if i:
                        yield i

    def get_node(self, path) -> 'Node':
        path_parts = path.split('.')
        if len(path_parts) == 1 and path == self.name:
            return self
        if len(path_parts) > 1 and path_parts[0] == self.name:
            if self.has_children:
                try:
                    _next = self.children[path_parts[1]]
                    return _next.get_node('.'.join(path_parts[1:]))
                except KeyError:
                    pass
        raise ValueError(f'No node found, deadend @ path {path}')

    def collect_matching(self, conditions):
        for path in self.find_children(conditions):
            yield (path, self.get_node(path))
