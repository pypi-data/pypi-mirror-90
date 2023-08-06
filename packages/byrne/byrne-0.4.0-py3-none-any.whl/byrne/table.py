from .helpers import set_optional_arg
from .dynamodb import DynamoDb
from .datastructures import TableDefinition
from .constants import DEFAULT_SELECT


class Table:
    """
        A low-level interface for interacting with DynamoDB Tables
    """
    def __init__(
        self,
        interface: DynamoDb,
        definition: TableDefinition,
        consistent_reads=True,
        read_limit=None
    ):
        self.definition = definition
        self.dynamodb = interface
        self.consistent_reads = consistent_reads
        self.read_limit = read_limit

    @property
    def name(self):
        return self.definition.name

    def query(
        self,
        key_condition_exp: str,
        select: str = DEFAULT_SELECT,
        scan_forward: bool = True,
        start=None,
        index: str = None,
        filter_exp: str = None,
        projection_exp: str = None,
        attr_names: dict = None,
        attr_values: dict = None
    ):
        query_args = {
            "TableName": self.name,
            "KeyConditionExpression": key_condition_exp,
            "Select": select,
            "ScanIndexForward": scan_forward
        }

        set_optional_arg("Limit", self.read_limit, query_args)
        set_optional_arg("ExclusiveStartKey", start, query_args)
        set_optional_arg("IndexName", index, query_args)
        set_optional_arg("FilterExpression", filter_exp, query_args)
        set_optional_arg("ExpressionAttributeNames", attr_names, query_args)
        set_optional_arg("ExpressionAttributeValues", attr_values, query_args)
        set_optional_arg("ProjectionExpression", projection_exp, query_args)

        return self.dynamodb.data_client.query(**query_args)

    def scan(
        self,
        select: str = DEFAULT_SELECT,
        start=None,
        index: str = None,
        filter_exp: str = None,
        projection_exp: str = None,
        attr_names: dict = None,
        attr_values: dict = None
    ):
        scan_args = {
            "TableName": self.name,
            "Select": select
        }

        set_optional_arg("Limit", self.read_limit, scan_args)
        set_optional_arg("ExclusiveStartKey", start, scan_args)
        set_optional_arg("IndexName", index, scan_args)
        set_optional_arg("FilterExpression", filter_exp, scan_args)
        set_optional_arg("ExpressionAttributeNames", attr_names, scan_args)
        set_optional_arg("ExpressionAttributeValues", attr_values, scan_args)
        set_optional_arg("ProjectionExpression", projection_exp, scan_args)

        return self.dynamodb.data_client.scan(**scan_args)

    def get_item(
        self,
        key: dict,
        projection_exp: str = None,
        attr_names: dict = None
    ):
        get_args = {
            "TableName": self.name,
            "ConsistentRead": self.consistent_reads,
            "Key": key,
        }

        set_optional_arg("ExpressionAttributeNames", attr_names, get_args)
        set_optional_arg("ProjectionExpression", projection_exp, get_args)

        return self.dynamodb.data_client.get_item(**get_args)

    def put_item(
        self,
        item: dict,
        condition_exp: str = None,
        attr_names: dict = None,
        attr_values: dict = None
    ):
        put_args = {
            "TableName": self.name,
            "Item": item
        }

        set_optional_arg("ConditionExpression", condition_exp, put_args)
        set_optional_arg("ExpressionAttributeNames", attr_names, put_args)
        set_optional_arg("ExpressionAttributeValues", attr_values, put_args)

        self.dynamodb.data_client.put_item(**put_args)

    def delete_item(
        self,
        key: dict,
        condition_exp: str = None,
        attr_names: dict = None,
        attr_values: dict = None
    ):
        delete_args = {
            "TableName": self.name,
            "Key": key,
        }

        set_optional_arg("ConditionExpression", condition_exp, delete_args)
        set_optional_arg("ExpressionAttributeNames", attr_names, delete_args)
        set_optional_arg("ExpressionAttributeValues", attr_values, delete_args)

        self.dynamodb.data_client.delete_item(**delete_args)

    def update_item(
        self,
        key: dict,
        update_exp: str,
        condition_exp: str = None,
        attr_names: dict = None,
        attr_values: dict = None
    ):
        update_args = {
            "TableName": self.name,
            "Key": key,
            "UpdateExpression": update_exp,
        }

        set_optional_arg("ConditionExpression", condition_exp, update_args)
        set_optional_arg("ExpressionAttributeNames", attr_names, update_args)
        set_optional_arg("ExpressionAttributeValues", attr_values, update_args)

        self.dynamodb.data_client.update_item(**update_args)

    @classmethod
    def get_table(cls, client: DynamoDb, name: str):
        return cls(client, client.get_table_definition(name))
