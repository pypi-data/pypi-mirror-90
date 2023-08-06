from abc import ABC, abstractmethod


class ObjectMap(ABC):
    @abstractmethod
    def map_item(self, item: dict):
        raise NotImplementedError

    @abstractmethod
    def unmap_object(self, obj) -> dict:
        raise NotImplementedError
