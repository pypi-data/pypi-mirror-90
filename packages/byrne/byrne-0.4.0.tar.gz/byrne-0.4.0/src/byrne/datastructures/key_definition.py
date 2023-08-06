from dataclasses import dataclass
from typing import Dict, List

from ..helpers import default


_KEY_DATATYPES = [
    "S",
    "N",
    "B"
]

_PARTITION_KEY = "HASH"
_SORT_KEY = "RANGE"


@dataclass
class KeyDefinition:
    partition_key: str
    sort_key: str = None
    projection: str = "ALL"
    include: List[str] = default(list)

    @property
    def is_sortable(self):
        if not self.sort_key:
            return False
        return True

    @property
    def attributes(self) -> List[str]:
        if self.is_sortable:
            return [self.partition_key, self.sort_key]
        return [self.partition_key]

    def is_valid(self, attributes: Dict[str, str]) -> bool:
        def is_key_valid(key):
            return key in attributes and attributes[key] in _KEY_DATATYPES
        if self.is_sortable:
            return is_key_valid(self.partition_key) and is_key_valid(self.sort_key)  # noqa: E501
        return is_key_valid(self.partition_key)

    def to_key_schema(self):
        def get_schema_item(name, partition=True):
            return {
                "AttributeName": name,
                "KeyType": "HASH" if partition else "RANGE",
            }
        schema = [get_schema_item(self.partition_key)]
        if self.is_sortable:
            schema.append(get_schema_item(self.sort_key, False))
        return schema

    def to_projection_schema(self):
        schema = {
            "ProjectionType": self.projection,
        }

        if self.projection == "INCLUDE":
            schema["NonKeyAttributes"] = self.include

        return schema

    @classmethod
    def from_key_schema(cls, schema: List[Dict[str, str]]):
        partition_key = None
        sort_key = None

        for key in schema:
            key_type = key["KeyType"]
            if key_type == _PARTITION_KEY:
                partition_key = key["AttributeName"]
            elif key_type == _SORT_KEY:
                sort_key = key["AttributeName"]

        assert(partition_key is not None)

        return cls(partition_key, sort_key)
