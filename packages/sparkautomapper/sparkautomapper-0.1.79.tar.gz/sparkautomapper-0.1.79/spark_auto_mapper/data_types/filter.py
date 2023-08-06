from typing import TypeVar, Generic, Callable, Any, Dict

from pyspark.sql import DataFrame, Column

from spark_auto_mapper.data_types.data_type_base import AutoMapperDataTypeBase

from spark_auto_mapper.type_definitions.wrapper_types import AutoMapperAnyDataType, AutoMapperColumnOrColumnLikeType
from spark_auto_mapper.helpers.spark_higher_order_functions import filter

_TAutoMapperDataType = TypeVar(
    "_TAutoMapperDataType", bound=AutoMapperAnyDataType
)


class AutoMapperFilterDataType(
    AutoMapperDataTypeBase, Generic[_TAutoMapperDataType]
):
    def __init__(
        self, column: AutoMapperColumnOrColumnLikeType,
        func: Callable[[Dict[str, Any]], Any]
    ) -> None:
        super().__init__()

        self.column: AutoMapperColumnOrColumnLikeType = column
        self.func: Callable[[Dict[str, Any]], Any] = func

    def get_column_spec(self, source_df: DataFrame) -> Column:
        return filter(
            self.column.get_column_spec(source_df=source_df), self.func
        )
