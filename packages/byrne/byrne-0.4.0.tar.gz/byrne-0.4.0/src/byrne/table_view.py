from .datastructures import Expression
from .table import Table
from .marshallers import Marshaller, AutoMarshaller
from .objectmaps import ObjectMap
from .paginators import Paginator, QueryPaginator, ScanPaginator  # noqa
from .constants import DEFAULT_SELECT, DEFAULT_PAGE  # noqa


class TableView:
    """
        A high-level interface for DynamoDB Tables
        Supports the following features:
            - Attribute marshalling/unmarshalling
            - Object mapping
            - Result pagination
    """

    def __init__(
        self,
        table: Table,
        marshaller: Marshaller = None,
        objectmap: ObjectMap = None,
        page_length: int = DEFAULT_PAGE,
        preload=True
    ):
        self.table = table
        self.marshaller = marshaller
        self.objectmap = objectmap
        self.secondary_indexes = []
        self.page_length = page_length
        self.preload = True

    def _postprocess_read_item(self, item: dict):
        if self.marshaller is not None:
            item = {
                k: self.marshaller.unpack_attribute(v)
                for k, v
                in item.items()
            }
        if self.objectmap is not None:
            return self.objectmap.map_item(item)
        return item

    def _preprocess_write_item(self, data):
        if self.objectmap is not None:
            data = self.objectmap.unmap_object(data)
        if self.marshaller is not None:
            return {
                k: self.marshaller.pack_attribute(v) for k, v in data.items()
            }
        return data

    @classmethod
    def get_default_table_view(cls, table: Table):
        return cls(table, AutoMarshaller())

    def _generate_items(self, paginator: Paginator):
        for item in paginator:
            yield self._postprocess_read_item(item)

    def _map_exp_values(self, values):
        return {
            k: self.marshaller.pack_attribute(v) for k, v in values.items()
        }

    def query(self, exp: Expression, index: str = None):
        kwargs = {
            "key_condition_exp": exp.expression,
            "attr_names": exp.attr_name_args,
            "attr_values": self._map_exp_values(exp.attr_value_args)
        }

        if index is not None:
            kwargs["index"] = index

        paginator = QueryPaginator(
            self.table,
            kwargs,
            self.page_length,
            self.preload
        )

        return self._generate_items(paginator)

    def scan(self, filter_exp: Expression = None):
        kwargs = {}

        if filter_exp is not None:
            kwargs = {
                "filter_condition": filter_exp.expression,
                "attr_names": filter_exp.attr_name_args,
                "attr_values": self._map_exp_values(filter_exp.attr_value_args)
            }

        paginator = ScanPaginator(
            self.table,
            kwargs,
            self.page_length,
            self.preload
        )

        return self._generate_items(paginator)

    def _get_primary_key_selector(self, value, sort=False):
        primary_key = self.table.definition.primary_key
        key_name = primary_key.partition_key

        if sort:
            assert primary_key.is_sortable
            key_name = primary_key.sort_key

        key_type = self.table.definition.attributes[key_name]

        return {key_name: self.marshaller.pack_attribute(value, key_type)}

    def _build_key_args(self, partition_key, sort_key):
        key_args = self._get_primary_key_selector(partition_key)
        if sort_key is not None:
            key_args.update(self._get_primary_key_selector(sort_key, True))
        return key_args

    def get_item(self, partition_key, sort_key=None):
        key_args = self._build_key_args(partition_key, sort_key)

        result = self.table.get_item(key_args)

        if "Item" in result:
            return self._postprocess_read_item(result["Item"])
        return None

    def put_item(self, item):
        self.table.put_item(self._preprocess_write_item(item))

    def update_item(self, exp: Expression, partition_key, sort_key=None):
        kwargs = {
            "key": self._build_key_args(partition_key, sort_key),
            "update_exp": exp.expression,
            "attr_names": exp.attr_name_args,
            "attr_values": self._map_exp_values(exp.attr_value_args)
        }

        self.table.update_item(**kwargs)

    def delete_item(self, partition_key, sort_key=None):
        key_args = self._build_key_args(partition_key, sort_key)
        self.table.delete_item(key_args)
