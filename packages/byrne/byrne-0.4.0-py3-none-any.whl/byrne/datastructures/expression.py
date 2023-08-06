import re
from dataclasses import dataclass

from ..helpers import default


def _make_regexp(start):
    return re.compile(f"(?<={start})\\w+")


RGX_NAME = _make_regexp("#")
RGX_VALUE = _make_regexp(":")


@dataclass
class Expression:
    expression: str
    name_mappings: dict = default(dict)
    value_mappings: dict = default(dict)

    def _get_rgx_matches(self, rgx):
        for result in rgx.finditer(self.expression):
            yield result.group()

    @property
    def name_keys(self):
        return [i for i in self._get_rgx_matches(RGX_NAME)]

    @property
    def value_keys(self):
        return [i for i in self._get_rgx_matches(RGX_VALUE)]

    @property
    def is_complete(self):
        def _check_mappings(expected_rgx, provided):
            for mapping in self._get_rgx_matches(expected_rgx):
                if mapping not in provided:
                    return False
            return True

        names_provided = _check_mappings(RGX_NAME, self.name_mappings)
        values_provided = _check_mappings(RGX_VALUE, self.value_mappings)

        return names_provided and values_provided

    @property
    def attr_name_args(self):
        return {f"#{k}": v for k, v in self.name_mappings.items()}

    @property
    def attr_value_args(self):
        return {f":{k}": v for k, v in self.value_mappings.items()}

    @staticmethod
    def merge_args(exp_a: "Expression", exp_b: "Expression"):
        def _is_conflict(dct_a: dict, dct_b: dict):
            for key in dct_a:
                if key in dct_b:
                    return True
            return False

        assert not _is_conflict(exp_a.name_mappings, exp_b.name_mappings)
        assert not _is_conflict(exp_a.value_mappings, exp_b.value_mappings)

        attr_names = {}
        attr_values = {}

        attr_names.update(exp_a.attr_name_args)
        attr_names.update(exp_b.attr_name_args)

        attr_values.update(exp_a.attr_value_args)
        attr_values.update(exp_b.attr_value_args)

        return (attr_names, attr_values)
