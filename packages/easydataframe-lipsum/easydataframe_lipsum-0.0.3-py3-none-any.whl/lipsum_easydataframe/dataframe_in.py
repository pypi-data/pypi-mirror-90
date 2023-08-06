from pathlib import Path
from typing import Callable

import pandas
from pandas import DataFrame


def _read_xlsx(path_: Path, sheet_name: str = None) -> DataFrame:
    """

    :param path_: xlsx path object
    :param sheet_name: target sheet name. default is Sheet1
    :return: result that read xlsx as dataframe
    """
    file_path: str = str(path_)

    df: DataFrame
    if sheet_name is None:
        df = pandas.read_excel(file_path, sheet_name="Sheet1", engine="openpyxl")

    else:
        df = pandas.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")

    return df


def _read_csv(path_: Path, sheet_name: str = None) -> DataFrame:
    """

    :param path_: csv path object
    :param sheet_name: None Only
    :return:
    """
    file_path: str = str(path_)
    return pandas.read_csv(file_path)


def _get_read_function(path_: Path) -> Callable[[Path, str], DataFrame]:
    """
    This function returns the appropriate function from the object.
    :param path_: target pathlib.Path object
    :return: .xlsx -> read_xlsx, .csv -> read_csv
    """
    function: Callable[[Path, str], DataFrame]
    suffix: str = path_.suffix

    if suffix == ".xlsx":
        function = _read_xlsx

    elif suffix == ".csv":
        function = _read_csv

    else:
        raise ValueError(str(path_) + " is not xlsx or not csv")

    return function


def read(file_path: str, sheet_name=None) -> DataFrame:
    """

    :param sheet_name: read target sheet name
    :param file_path: target file path
    :return: result that read xlsx or csv as dataframe
    """
    path_ = Path(file_path)

    function: Callable[[Path, str], DataFrame] = _get_read_function(path_)
    return function(path_, sheet_name)
