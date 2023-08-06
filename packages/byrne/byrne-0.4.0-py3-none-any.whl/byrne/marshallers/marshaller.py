from abc import ABC, abstractmethod
from numbers import Number

from ..helpers import first_kvp


class Marshaller(ABC):
    """
        A Marshaller is responsible for translating between
        the "packed" representation of attribute values from DynamoDB
        and a "native" Python representation of that value and vice versa.

        For example, consider the following attribute value from DDB:
            {'BS': ['MQ==', 'Mg==', 'Mw==']}
        This is represented in Python as:
            [b"1", b"2", b"3"]
    """
    @abstractmethod
    def detect_attribute_type(self, value) -> str:
        raise NotImplementedError

    @abstractmethod
    def pack_string(self, value: str):
        raise NotImplementedError

    @abstractmethod
    def pack_number(self, value: Number):
        raise NotImplementedError

    @abstractmethod
    def pack_binary(self, value: bytes):
        raise NotImplementedError

    @abstractmethod
    def pack_bool(self, value: bool):
        raise NotImplementedError

    def pack_null(self, value: type(None)):
        return True

    def pack_string_set(self, value: list):
        return [self.pack_string(x) for x in value]

    def pack_number_set(self, value: list):
        return [self.pack_number(x) for x in value]

    def pack_binary_set(self, value: list):
        return [self.pack_binary(x) for x in value]

    def pack_map(self, value: dict):
        return {k: self.pack_attribute(v) for k, v in value.items()}

    def pack_list(self, value: list):
        return [self.pack_attribute(i) for i in value]

    @abstractmethod
    def unpack_string(self, value):
        raise NotImplementedError

    @abstractmethod
    def unpack_number(self, value):
        raise NotImplementedError

    @abstractmethod
    def unpack_binary(self, value):
        raise NotImplementedError

    @abstractmethod
    def unpack_bool(self, value):
        raise NotImplementedError

    def unpack_null(self, value):
        return None

    def unpack_string_set(self, value: list):
        return [self.unpack_string(x) for x in value]

    def unpack_number_set(self, value: list):
        return [self.unpack_number(x) for x in value]

    def unpack_binary_set(self, value: list):
        return [self.unpack_binary(x) for x in value]

    def unpack_map(self, data):
        return {k: self.unpack_attribute(v) for k, v in data.items()}

    def unpack_list(self, data):
        return [self.unpack_attribute(i) for i in data]

    def unpack_attribute(self, attribute):
        attribute_type, attribute_value = first_kvp(attribute)

        return {
            "S": self.unpack_string,
            "N": self.unpack_number,
            "B": self.unpack_binary,
            "SS": self.unpack_string_set,
            "NS": self.unpack_number_set,
            "BS": self.unpack_binary_set,
            "M": self.unpack_map,
            "L": self.unpack_list,
            "NULL": self.unpack_null,
            "BOOL": self.unpack_bool
        }[attribute_type](attribute_value)

    def pack_attribute(self, value, force_type=None):
        attribute_type = force_type

        if force_type is None:
            attribute_type = self.detect_attribute_type(value)

        attribute_value = {
            "S": self.pack_string,
            "N": self.pack_number,
            "B": self.pack_binary,
            "SS": self.pack_string_set,
            "NS": self.pack_number_set,
            "BS": self.pack_binary_set,
            "M": self.pack_map,
            "L": self.pack_list,
            "NULL": self.pack_null,
            "BOOL": self.pack_bool
        }[attribute_type](value)
        return {attribute_type: attribute_value}
