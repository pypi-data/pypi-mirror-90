from typing import Generic, TypeVar

from pyspark.sql import DataFrame, Column

from spark_auto_mapper.data_types.data_type_base import AutoMapperDataTypeBase
from spark_auto_mapper.helpers.spark_higher_order_functions import transform
from spark_auto_mapper.type_definitions.wrapper_types import AutoMapperAnyDataType, AutoMapperColumnOrColumnLikeType

_TAutoMapperDataType = TypeVar(
    "_TAutoMapperDataType", bound=AutoMapperAnyDataType
)


class AutoMapperTransformDataType(
    AutoMapperDataTypeBase, Generic[_TAutoMapperDataType]
):
    def __init__(
        self, column: AutoMapperColumnOrColumnLikeType,
        value: _TAutoMapperDataType
    ) -> None:
        super().__init__()

        self.column: AutoMapperColumnOrColumnLikeType = column
        self.value: _TAutoMapperDataType = value

    def get_column_spec(self, source_df: DataFrame) -> Column:
        column_spec: Column = self.column.get_column_spec(source_df=source_df)
        value_get_column_spec: Column = self.value.get_column_spec(
            source_df=source_df
        )
        return transform(column_spec, lambda y: value_get_column_spec)
