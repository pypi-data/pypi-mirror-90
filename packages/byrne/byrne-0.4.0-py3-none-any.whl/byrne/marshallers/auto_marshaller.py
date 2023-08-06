from numbers import Number
from base64 import b64encode, b64decode

from .marshaller import Marshaller

from ..helpers import autoclassifier
from ..constants import SET_SUBTYPES, ENCODING


class AutoMarshaller(Marshaller):
    """
        This is the default Marshaller implementation.

        This implementation uses datatype checking to infer DynamoDB
        attribute types. This implementation can automatically pack
        appropriate lists into set types if enabled. For example, if
        a value to be packed is a list of strings, this will be stored
        as a String Set.

        Additionally, the casting of DynamoDB Numbers to Python types is
        customisable.
    """

    _DEFAULT_CLASSIFIERS = {
        "S": autoclassifier(str),
        "N": lambda x: (not isinstance(x, bool)) and isinstance(x, Number),
        "B": autoclassifier(bytes),
        "M": autoclassifier(dict),
        "L": autoclassifier(list),
        "NULL": autoclassifier(type(None)),
        "BOOL": autoclassifier(bool)
    }

    def __init__(self, auto_set_detect: bool = True, number_cast=float):
        self.auto_set_detect = auto_set_detect
        self.number_cast = number_cast

    def _detect_default_type(self, value):
        for typekey, classifier in self._DEFAULT_CLASSIFIERS.items():
            if classifier(value):
                return typekey

    def _detect_set_type(self, value: list):
        last_subtype = None

        def is_not_valid_set(subtype):
            is_not_set_type = subtype not in SET_SUBTYPES
            is_not_first = last_subtype is not None
            is_not_match = subtype != last_subtype

            return is_not_set_type or (is_not_first and is_not_match)

        for item in value:
            subtype = self._detect_attribute_type(item, True)
            if is_not_valid_set(subtype):
                return "L"
            last_subtype = subtype
        return f"{last_subtype}S"

    def _detect_attribute_type(self, value, override_set_detect=False):
        should_check_set = not override_set_detect and self.auto_set_detect
        if should_check_set and isinstance(value, list):
            return self._detect_set_type(value)
        return self._detect_default_type(value)

    def detect_attribute_type(self, value):
        return self._detect_attribute_type(value)

    def pack_string(self, value: str):
        return str(value)

    def pack_number(self, value: Number):
        try:
            if int(value) == value:
                value = int(value)
        finally:
            return str(value)

    def pack_binary(self, value: bytes):
        return b64encode(value).decode(ENCODING)

    def pack_bool(self, value: bool):
        return bool(value)

    def unpack_string(self, value):
        return str(value)

    def unpack_number(self, value):
        return self.number_cast(value)

    def unpack_binary(self, value):
        return b64decode(value.encode(ENCODING))

    def unpack_bool(self, value):
        return bool(value)
