from __future__ import annotations
from typing import Type, TypeVar

import numpy as np
import pandas as pd
from pyarrow import Schema


class ColumnType(pd.Series):
    pass


class StringColumn(ColumnType):
    df_type = str


class IntColumn(ColumnType):
    df_type = int


class BoolColumn(ColumnType):
    df_type = bool


class FloatColumn(ColumnType):
    df_type = float


class DataframeSchema(pd.DataFrame):
    df: pd.DataFrame
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def __setattr__(self, key, value):
        if key == "df":
            return object.__setattr__(self, key, value)
        else:
            return self.df.__setattr__(key, value)

    def __getattribute__(self, item):
        if item == "df":
            return object.__getattribute__(self,  item)
        value = self.df.__getattribute__(item)
        if callable(value) and hasattr(value, "__self__") and value.__self__ is not None:
            value = self._wrap_callable(value)
        return value

    @classmethod
    def _wrap_callable(cls, function):
        def wrapper(*args, **kwargs):
            results = function(*args, **kwargs)
            if isinstance(results, pd.DataFrame):
                results = cls(results)
            return results
        return wrapper

    @classmethod
    def from_columns(cls: Type[SchemaType], *columns) -> SchemaType:
        df_dict = {}
        for (column_name, column_type), column in zip(cls.__annotations__.items(), columns):
            df_dict[column_name] = column
        return cls(pd.DataFrame.from_dict(df_dict))

    @classmethod
    def zeros(cls: Type[SchemaType], length: int) -> SchemaType:
        df_dict = {}
        for column_name, column_type in cls.__annotations__.items():
            df_dict[column_name] = np.zeros(length, dtype=column_type.df_type)
        return cls(pd.DataFrame.from_dict(df_dict))



SchemaType = TypeVar("SchemaType", bound=DataframeSchema)
