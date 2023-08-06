from dataclasses import dataclass
from typing import Dict, List

from .key_definition import KeyDefinition
from ..helpers import default


@dataclass
class TableDefinition:
    name: str = None
    attributes: Dict[str, str] = default(dict)
    primary_key: KeyDefinition = None
    gsi: Dict[str, KeyDefinition] = default(dict)
    lsi: Dict[str, KeyDefinition] = default(dict)
    arn: str = None
    status: str = None

    @property
    def key_attributes(self) -> List[str]:
        attrs = self.primary_key.attributes

        for key in self.secondary_keys:
            attrs += key.attributes

        return list(set(attrs))

    @property
    def gsi_keys(self) -> List[KeyDefinition]:
        return list(self.gsi.values())

    @property
    def lsi_keys(self) -> List[KeyDefinition]:
        return list(self.lsi.values())

    @property
    def secondary_keys(self) -> List[KeyDefinition]:
        return self.gsi_keys + self.lsi_keys

    @property
    def is_valid(self) -> bool:
        if not self.primary_key.is_valid(self.attributes):
            return False

        for key in self.secondary_keys:
            if not key.is_valid(self.attributes):
                return False
        return True

    @property
    def keys(self) -> List[KeyDefinition]:
        return [self.primary_key] + self.secondary_keys

    def get_secondary_key(self, name):
        if name in self.lsi:
            return self.lsi[name]
        return self.gsi[name]

    def get_projected_attributes(self, index) -> List[str]:
        key = None

        if index in self.gsi:
            key = self.gsi[index]
        else:
            key = self.lsi[index]

        if key.projection == "ALL":
            return list(self.attributes.keys())
        else:
            base_keys = [self.primary_key.partition_key]
            if key.projection == "KEYS_ONLY":
                return base_keys + key.attributes
            elif key.projection == "INCLUDE":
                return base_keys + key.attributes + key.include
