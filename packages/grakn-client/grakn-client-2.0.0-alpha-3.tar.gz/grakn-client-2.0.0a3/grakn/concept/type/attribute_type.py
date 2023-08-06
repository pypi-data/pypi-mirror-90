#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from datetime import datetime

import graknprotocol.protobuf.concept_pb2 as concept_proto

from grakn.concept.proto import concept_proto_builder, concept_proto_reader
from grakn.concept.type.thing_type import ThingType, RemoteThingType
from grakn.concept.type.value_type import ValueType


def is_keyable(value_type: ValueType):
    return value_type in [ValueType.LONG, ValueType.STRING, ValueType.DATETIME]


class AttributeType(ThingType):

    def as_remote(self, transaction):
        return RemoteAttributeType(transaction, self.get_label(), self.is_root())

    def get_value_type(self):
        return ValueType.OBJECT

    def is_keyable(self):
        return is_keyable(self.get_value_type())

    def is_attribute_type(self):
        return True

    def is_boolean(self):
        return False

    def is_long(self):
        return False

    def is_double(self):
        return False

    def is_string(self):
        return False

    def is_datetime(self):
        return False

    def __eq__(self, other):
        if other is self:
            return True
        # root "attribute" should always be equal to itself regardless of which value class it holds
        if not other or not isinstance(AttributeType, other):
            return False
        return self.get_label() == other.get_label()

    def __hash__(self):
        return super(AttributeType, self).__hash__()


class RemoteAttributeType(RemoteThingType):

    def get_value_type(self):
        return ValueType.OBJECT

    def is_keyable(self):
        return is_keyable(self.get_value_type())

    def as_remote(self, transaction):
        return RemoteAttributeType(transaction, self.get_label(), self.is_root())

    def get_owners(self, only_key=False):
        method = concept_proto.Type.Req()
        get_owners_req = concept_proto.AttributeType.GetOwners.Req()
        get_owners_req.only_key = only_key
        method.attribute_type_get_owners_req.CopyFrom(get_owners_req)
        return self._type_stream(method, lambda res: res.attribute_type_get_owners_res.owners)

    def _put_internal(self, value_proto):
        method = concept_proto.Type.Req()
        put_req = concept_proto.AttributeType.Put.Req()
        put_req.value.CopyFrom(value_proto)
        method.attribute_type_put_req.CopyFrom(put_req)
        return concept_proto_reader.attribute(self._execute(method).attribute_type_put_res.attribute)

    def _get_internal(self, value_proto):
        method = concept_proto.Type.Req()
        get_req = concept_proto.AttributeType.Get.Req()
        get_req.value.CopyFrom(value_proto)
        method.attribute_type_get_req.CopyFrom(get_req)
        response = self._execute(method).attribute_type_get_res
        return concept_proto_reader.attribute(response.attribute) if response.WhichOneof("res") == "attribute" else None

    def is_attribute_type(self):
        return True

    def is_boolean(self):
        return False

    def is_long(self):
        return False

    def is_double(self):
        return False

    def is_string(self):
        return False

    def is_datetime(self):
        return False

    def __eq__(self, other):
        if other is self:
            return True
        if not other or not isinstance(RemoteAttributeType, other):
            return False
        return self.get_label() == other.get_label()

    def __hash__(self):
        return super(RemoteAttributeType, self).__hash__()


class BooleanAttributeType(AttributeType):

    @staticmethod
    def _of(type_proto: concept_proto.Type):
        return BooleanAttributeType(type_proto.label, type_proto.root)

    def get_value_type(self):
        return ValueType.BOOLEAN

    def as_remote(self, transaction):
        return RemoteBooleanAttributeType(transaction, self.get_label(), self.is_root())

    def is_boolean(self):
        return True


class RemoteBooleanAttributeType(RemoteAttributeType):

    def get_value_type(self):
        return ValueType.BOOLEAN

    def as_remote(self, transaction):
        return RemoteBooleanAttributeType(transaction, self.get_label(), self.is_root())

    def put(self, value: bool):
        return self._put_internal(concept_proto_builder.boolean_attribute_value(value))

    def get(self, value: bool):
        return self._get_internal(concept_proto_builder.boolean_attribute_value(value))

    def is_boolean(self):
        return True


class LongAttributeType(AttributeType):

    @staticmethod
    def _of(type_proto: concept_proto.Type):
        return LongAttributeType(type_proto.label, type_proto.root)

    def get_value_type(self):
        return ValueType.LONG

    def as_remote(self, transaction):
        return RemoteLongAttributeType(transaction, self.get_label(), self.is_root())

    def is_long(self):
        return True


class RemoteLongAttributeType(RemoteAttributeType):

    def get_value_type(self):
        return ValueType.LONG

    def as_remote(self, transaction):
        return RemoteLongAttributeType(transaction, self.get_label(), self.is_root())

    def put(self, value: int):
        return self._put_internal(concept_proto_builder.long_attribute_value(value))

    def get(self, value: int):
        return self._get_internal(concept_proto_builder.long_attribute_value(value))

    def is_long(self):
        return True


class DoubleAttributeType(AttributeType):

    @staticmethod
    def _of(type_proto: concept_proto.Type):
        return DoubleAttributeType(type_proto.label, type_proto.root)

    def get_value_type(self):
        return ValueType.DOUBLE

    def as_remote(self, transaction):
        return RemoteDoubleAttributeType(transaction, self.get_label(), self.is_root())

    def is_double(self):
        return True


class RemoteDoubleAttributeType(RemoteAttributeType):

    def get_value_type(self):
        return ValueType.DOUBLE

    def as_remote(self, transaction):
        return RemoteDoubleAttributeType(transaction, self.get_label(), self.is_root())

    def put(self, value: float):
        return self._put_internal(concept_proto_builder.double_attribute_value(value))

    def get(self, value: float):
        return self._get_internal(concept_proto_builder.double_attribute_value(value))

    def is_double(self):
        return True


class StringAttributeType(AttributeType):

    @staticmethod
    def _of(type_proto: concept_proto.Type):
        return StringAttributeType(type_proto.label, type_proto.root)

    def get_value_type(self):
        return ValueType.STRING

    def as_remote(self, transaction):
        return RemoteStringAttributeType(transaction, self.get_label(), self.is_root())

    def is_string(self):
        return True


class RemoteStringAttributeType(RemoteAttributeType):

    def get_value_type(self):
        return ValueType.STRING

    def as_remote(self, transaction):
        return RemoteStringAttributeType(transaction, self.get_label(), self.is_root())

    def put(self, value: str):
        return self._put_internal(concept_proto_builder.string_attribute_value(value))

    def get(self, value: str):
        return self._get_internal(concept_proto_builder.string_attribute_value(value))

    def is_string(self):
        return True


class DateTimeAttributeType(AttributeType):

    @staticmethod
    def _of(type_proto: concept_proto.Type):
        return DateTimeAttributeType(type_proto.label, type_proto.root)

    def get_value_type(self):
        return ValueType.DATETIME

    def as_remote(self, transaction):
        return RemoteDateTimeAttributeType(transaction, self.get_label(), self.is_root())

    def is_datetime(self):
        return True


class RemoteDateTimeAttributeType(RemoteAttributeType):

    def get_value_type(self):
        return ValueType.DATETIME

    def as_remote(self, transaction):
        return RemoteDateTimeAttributeType(transaction, self.get_label(), self.is_root())

    def put(self, value: datetime):
        return self._put_internal(concept_proto_builder.datetime_attribute_value(value))

    def get(self, value: datetime):
        return self._get_internal(concept_proto_builder.datetime_attribute_value(value))

    def is_datetime(self):
        return True
