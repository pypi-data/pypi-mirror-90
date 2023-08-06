from typing import Optional

from pyspark.sql import Column, DataFrame
# noinspection PyUnresolvedReferences
from pyspark.sql.functions import col

from spark_auto_mapper.data_types.array_base import AutoMapperArrayBase


class AutoMapperDataTypeColumn(AutoMapperArrayBase):
    def __init__(self, value: str):
        super().__init__()
        if len(value) > 0 and value[0] == "[":
            self.value: str = value[1:-1]  # skip the first and last characters
        else:
            self.value = value

    def get_column_spec(
        self, source_df: DataFrame, current_column: Optional[Column]
    ) -> Column:
        if isinstance(self.value, str):
            if self.value.startswith("_") and current_column is not None:
                elements = self.value.split(".")
                if len(elements) > 0:
                    return current_column[elements[1]]
                else:
                    return current_column
            elif not self.value.startswith("a.") and not self.value.startswith(
                "b."
            ):
                # prepend with "b." in case the column exists in both a and b tables
                return col("b." + self.value)
            else:
                return col(self.value)

        raise ValueError(f"value: {self.value} is not str")
