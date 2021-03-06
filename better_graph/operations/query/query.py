from typing import Dict, List, Iterable

from pydantic import BaseModel

from better_graph.operations.query.query_model_constructor import QueryInputModelConstructor, QueryOutputModelConstructor, \
    QueryInputModel
from better_graph.operations.query.query_resolver import QueryResolver


class Query:
    """
    TODO: Change ModelConstructors to not include "name" and "fields" but only provides the interesting variables
            For example please change "fields" in ModelConstructor to "projection"
    """
    def __init__(
            self,
            name: str,
            base_adapter,
            fields: Dict[str, str],
            excluded_input_fields: List[str],
            excluded_output_fields: List[str],
            excluded_query_params: List[str] = None
    ):

        self.input_model: QueryInputModel = QueryInputModelConstructor(
            name=name,
            projection=fields,
            excluded_input_fields=excluded_input_fields
        )
        self.output_model: BaseModel = QueryOutputModelConstructor(
            name=name,
            fields=fields,
            excluded_output_fields=excluded_output_fields
        )

        self.resolver = QueryResolver(
            name=name,
            base_adapter=base_adapter,
            fields=self.output_model.__annotations__,
            excluded_query_params=excluded_query_params
        )

    def __call__(self, input_dict: dict):
        input_: QueryInputModel = self.input_model(**input_dict)
        cursor: Iterable = self.resolver(input_)
        return [self.output_model(**x).dict(skip_defaults=True) for x in cursor]
