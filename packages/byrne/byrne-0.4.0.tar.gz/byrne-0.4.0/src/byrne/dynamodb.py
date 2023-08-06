import time
from typing import List

from boto3 import Session
from amazondax import AmazonDaxClient

from .helpers import set_arg_if_not_empty
from .datastructures import TableDefinition, KeyDefinition
from .constants import DYNAMODB_RESVD_WORDS


class DynamoDb:
    def __init__(self, client, dax: AmazonDaxClient = None):
        self.client = client
        self.dax = dax

    def list_tables(self) -> List[str]:
        return self.client .list_tables()["TableNames"]

    def get_table_definition(self, name):
        definition = TableDefinition()
        response = self.client.describe_table(TableName=name)
        table = response["Table"]

        definition.name = table["TableName"]
        definition.arn = table["TableArn"]
        definition.status = table["TableStatus"]

        if "AttributeDefinitions" in table:
            for attr in table["AttributeDefinitions"]:
                attr_name = attr["AttributeName"]
                definition.attributes[attr_name] = attr["AttributeType"]

        if "KeySchema" in table:
            definition.primary_key = KeyDefinition.from_key_schema(
                table["KeySchema"]
            )

        indexes = (("Global", definition.gsi), ("Local", definition.lsi))

        for index_scope, index_dict in indexes:
            index_type = f"{index_scope}SecondaryIndexes"
            if index_type in table:
                for index in table[index_type]:
                    keydef = KeyDefinition.from_key_schema(index["KeySchema"])
                    index_dict[index["IndexName"]] = keydef

        return definition

    def create_table(self, definition: TableDefinition, **kwargs):
        creation_args = self.get_creation_args_for_definition(definition)
        creation_args.update(kwargs)
        self.client.create_table(**creation_args)
        return self.get_table_definition(definition.name)

    def delete_table(self, table):
        table = self._normalise_table_name(table)
        self.client.delete_table(TableName=table)

    def wait_for_states(self, table, states):
        table = self._normalise_table_name(table)
        ready = False

        while not ready:
            tabledef = self.get_table_definition(table)
            ready = tabledef.status in states
            time.sleep(1)

    def wait_for_active(self, table):
        return self.wait_for_states(table, ["ACTIVE"])

    def wait_for_deletion(self, table):
        table = self._normalise_table_name(table)
        ready = False

        while not ready:
            try:
                self.get_table_definition(table)
                time.sleep(1)
            except self._not_found:
                ready = True

    @property
    def _not_found(self):
        return self.client.exceptions.ResourceNotFoundException

    @staticmethod
    def _normalise_table_name(table):
        if isinstance(table, TableDefinition):
            table = table.name
        return table

    @staticmethod
    def get_creation_args_for_definition(definition: TableDefinition):
        def get_attr_args(key_attribute: str):
            return {
                "AttributeName": key_attribute,
                "AttributeType": definition.attributes[key_attribute]
            }

        def get_index_args(name: str, keydef: KeyDefinition):
            return {
                "IndexName": name,
                "KeySchema": keydef.to_key_schema(),
                "Projection": keydef.to_projection_schema()
            }

        attrs = [get_attr_args(item) for item in definition.key_attributes]

        creation_args = {
            "AttributeDefinitions": attrs,
            "TableName": definition.name,
            "KeySchema": definition.primary_key.to_key_schema(),
            "BillingMode": "PAY_PER_REQUEST"
        }

        lsi = [
            get_index_args(key, value)
            for key, value
            in definition.lsi.items()
        ]

        gsi = [
            get_index_args(key, value)
            for key, value
            in definition.gsi.items()
        ]

        set_arg_if_not_empty("LocalSecondaryIndexes", lsi, creation_args)
        set_arg_if_not_empty("GlobalSecondaryIndexes", gsi, creation_args)

        return creation_args

    @classmethod
    def get_default_client(cls, dax_endpoints=None):
        return cls.get_client_from_session(Session())

    @classmethod
    def get_client_from_session(cls, session: Session, dax_endpoints=None):
        dax = None
        if dax_endpoints is not None:
            dax = AmazonDaxClient(session, endpoints=dax_endpoints)
        return cls(session.client("dynamodb"), dax)

    @property
    def data_client(self):
        if self.dax is not None:
            return self.dax
        return self.client

    @staticmethod
    def requires_exp_attr_name(attr_name: str):
        assert len(attr_name) >= 1

        if attr_name.upper() in DYNAMODB_RESVD_WORDS or "." in attr_name:
            return True

        return False
