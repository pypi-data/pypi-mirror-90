from typing import List, Union, Any

import numpy
import pandas
from pandas import DataFrame, Series
from numpy import NaN

"""
This py file provides dataframe and list related functionality.

pandas.DataFrame Suitable for beginners.
"""


def _get_test_number_dataframe() -> DataFrame:
    """

    :return:
    """
    col_list: List[str] = []
    rec_list: List[str] = []
    data_list: List[List[int]] = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [8, 9, 10, 11]
    ]
    return DataFrame(data=data_list, columns=col_list, index=rec_list)


def _get_test_NaN_in_dataframe() -> DataFrame:
    """

    :return:
    """

    col_list: List[str] = ["columnLabel0", "columnLabel1", "columnLabel2", "columnLabel3"]
    rec_list: List[str] = ["recordLabel0", "recordLabel1", "recordLabel2"]
    data_list: List[List[Union[str, NaN]]] = [
        ["0-0", "0-1", "0-2", NaN],
        ["1-0", "1-1", NaN, "1-3"],
        ["2-0", NaN, "2-2", "2-3"]
    ]
    return DataFrame(data=data_list, columns=col_list, index=rec_list)


def _get_test_dataframe() -> DataFrame:
    """
    This function is used in doctest
    :return: example DataFrame
    """
    col_list: List[str] = ["columnLabel0", "columnLabel1", "columnLabel2", "columnLabel3"]
    rec_list: List[str] = ["recordLabel0", "recordLabel1", "recordLabel2"]
    data_list: List[List[str]] = [
        ["0-0", "0-1", "0-2", "0-3"],
        ["1-0", "1-1", "1-2", "1-3"],
        ["2-0", "2-1", "2-2", "2-3"]
    ]
    return DataFrame(data=data_list, columns=col_list, index=rec_list)


def is_NaN_or_none(df: DataFrame) -> bool:
    """

    :param df:
    :return:

    >>> is_NaN_or_none(_get_test_dataframe())
    False

    >>> is_NaN_or_none(_get_test_NaN_in_dataframe())
    True
    """

    for i in get_record_names(df):
        for j in get_column_names(df):
            _str = read_cell(df=df, record_name=i, column_name=j)
            if _str == "nan" or _str == "None":
                return True
        continue

    return False


def dataframe_to_2dim_list(df: DataFrame) -> List[List[str]]:
    """

    :param df: target dataframe
    :return: dataframe -> List[List[elements]]

    >>> dataframe_to_2dim_list(_get_test_dataframe())
    [['0-0', '0-1', '0-2', '0-3'], ['1-0', '1-1', '1-2', '1-3'], ['2-0', '2-1', '2-2', '2-3']]
    """

    result_2dim: List[List[str]] = []

    for i in get_record_names(df):
        inner_list: List[Any] = []
        for j in get_column_names(df):
            _str = read_cell(df=df, record_name=i, column_name=j)
            inner_list.append(_str)

        result_2dim.append(inner_list)
        continue

    return result_2dim


def _any_to_str(_any: Any) -> str:
    if type(_any) is not str:
        return str(_any)

    return _any


def len_record(df: DataFrame) -> int:
    """
    :param df: pandas.DataFrame
    :return: Count the number of rows in a dataframe

    >>> len_record(_get_test_dataframe())
    3
    """
    return len(df)


def len_column(df: DataFrame) -> int:
    """
    :param df: pandas.DataFrame
    :return: Count the number of columns in a dataframe

    >>> len_column(_get_test_dataframe())
    4
    """
    return len(df.columns)


def read_cell(df: DataFrame, record_name: str, column_name: str) -> str:
    """
    This function extracts specific data from a dataframe.

    :param df: target dataframe to extract
    :param record_name: Rows name to extract
    :param column_name: Column name to extract
    :return: matched data

    >>> read_cell(_get_test_dataframe(), record_name='recordLabel1', column_name='columnLabel2')
    '1-2'
    """
    return _any_to_str(df.loc[record_name, column_name])


def read_cell_from_raw_number(df: DataFrame, record_number: int, column_number: int) -> str:
    """

    :param df:
    :param record_number:
    :param column_number:
    :return

    >>> read_cell_from_raw_number(_get_test_dataframe(), record_number=1, column_number=2)
    '1-2'
    """

    series: Series = df.iloc[record_number]
    return _any_to_str(series.iloc[column_number])


def read_records(row_dataframe: DataFrame, column_name: str) -> List[str]:
    """

    :param row_dataframe: target dataframe to extract
    :param column_name: Column name to extract
    :return: matching column name list

    >>> read_records(_get_test_dataframe(), column_name='columnLabel1')
    ['0-1', '1-1', '2-1']
    """
    len_record(row_dataframe)
    result: List[str] = []

    for i in get_record_names(row_dataframe):
        result.append(read_cell(df=row_dataframe, record_name=i, column_name=column_name))

    return result


def read_columns(row_dataframe: DataFrame, record_index: Union[int, str]) -> List[str]:
    """

    :param row_dataframe: target dataframe to extract
    :param record_index: Column name to extract
    :return: Returns the specified column in the data frame as a str list

    >>> read_columns(row_dataframe=_get_test_dataframe(), record_index='recordLabel1')
    ['1-0', '1-1', '1-2', '1-3']
    """
    result: List[str] = []
    for i in get_column_names(row_dataframe):
        result.append(read_cell(df=row_dataframe, record_name=record_index, column_name=i))

    return result


def __numpy_to_list(numpy_array: numpy.ndarray) -> List[str]:
    """

    :param numpy_array: dataframe.values
    :return: Transaction List[str]

    >>> nd: numpy.ndarray = Series(data=[0,1,2]).values
    >>> __numpy_to_list(nd)
    ['0', '1', '2']
    """
    result: List[str] = []

    for i in numpy_array:
        result.append(_any_to_str(i))

    return result


def _series_to_list(series: Series) -> List[str]:
    """

    :param series:
    :return: pandas.Series -> typing.List
    """
    return __numpy_to_list(series.values)


def get_column_names(df: DataFrame) -> List[str]:
    """
    :param df: pandas.DataFrame
    :return: list of column names in the dataframe

    >>> get_column_names(_get_test_dataframe())
    ['columnLabel0', 'columnLabel1', 'columnLabel2', 'columnLabel3']

    """
    return __numpy_to_list(df.columns.values)


def get_record_names(df: DataFrame) -> List[str]:
    """
    :param df: pandas.DataFrame
    :return: list of rows names in the dataframe

    >>> get_record_names(_get_test_dataframe())
    ['recordLabel0', 'recordLabel1', 'recordLabel2']
    """
    return __numpy_to_list(df.index.values)


def get_record_from_index(df: DataFrame, index_number: Union[int, str]) -> Series:
    """
    :param df: pandas.DataFrame
    :param index_number: N rows
    :return: The Nth line of the dataframe as a Series type

    doctest is None
    get_record_from_index(df=_get_test_dataframe(), index_number='recordLabel1')
    ->
    columnLabel0    1-0
    columnLabel1    1-1
    columnLabel2    1-2
    columnLabel3    1-3
    """
    return df.loc[index_number]


def get_column_from_keyword(df: pandas.DataFrame, keyword: str) -> DataFrame:
    """

    :param df: pandas.DataFrame
    :param keyword: Column name to extract
    :return: Returns a list of matched columns from the data frame
    """
    return df.loc[:, keyword]


class NaNError(Exception):
    """
    This error is thrown when NaN is not allowed.
    """
    pass


class NotNaNDataFrameFactory:
    """
    This class create DataFrame. reject NaN Data.

    >>> factory = NotNaNDataFrameFactory(column_name_list=['a', 'b'], record_name_list=['1'])
    >>> df = factory.create(data_list=[['dog', 'cat']])
    >>> read_cell_from_raw_number(df=df, record_number=0, column_number=1)
    'cat'
    """

    __columns: List[str]
    __records: List[str]

    def __init__(self, column_name_list: List[str], record_name_list: List[str]):
        self.__columns = column_name_list
        self.__records = record_name_list
        return

    def create(self, data_list: List[List]) -> DataFrame:
        """
        :param data_list: creation target list
        :return:

        """

        record_of_number: int = len(self.__records)
        if len(data_list) != record_of_number:
            raise NaNError("column is not" + str(record_of_number))

        column_of_number: int = len(self.__columns)
        for i in data_list:
            if len(i) != column_of_number:
                raise NaNError("record is not" + str(column_of_number))
            continue

        return DataFrame(data=data_list, index=self.__records, columns=self.__columns)


class DataFrameLabel:
    column_name_list: List[str]
    rows_name_list: List[str]
    dataframe: DataFrame

    def __init__(self, df: DataFrame) -> None:
        self.dataframe = df
        self.column_name_list = get_column_names(self.dataframe)
        self.rows_name_list = get_record_names(self.dataframe)
        return


if __name__ == '__main__':
    import doctest

    doctest.testmod()
