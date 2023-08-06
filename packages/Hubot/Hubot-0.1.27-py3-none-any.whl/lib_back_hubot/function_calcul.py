import numpy as np
import pandas as pd
from typing import List


def sum_column(data: pd.DataFrame, col: str) -> dict:
    """
    Sum values of a cube column

    Parameters
    ----------
    data: filtered cube with multiple columns
    col: name of the cube column to sum

    Returns
    -------
    dict : {"result": <float: result of sum>} or {"error": <str: reason of error">}

    Example
    -------
    >>> sum_column(pd.DataFrame({'col1': pd.Series([1, 2])}), 'col1')
    {"result": 3}
    """

    if col not in data.columns:
        return {"error": "nonexistent column: " + col}

    if data.dtypes[col] not in ["int64", "float64"]:
        return {"error": "data with invalid type"}

    return {"result": float(data[col].sum())}


def rate_column(data: pd.DataFrame, col1: str, col2: str) -> dict:
    """
    Compute the rate of two summed columns values

    Parameters
    ----------
    data: filtered cube with multiple columns
    col1: column name corresponding to the nominator of the rate
    col2: column name corresponding to the denominator of the rate

    Returns
    -------
    dict : {"result": <float: rate>} or {"error": <reason of error">}

    Example
    -------
    >>> rate_column(df, 'col1', 'col2')
    {"result": 0.43}
    """

    # First the columns are summed, obtaining two float
    sum1 = sum_column(data, col1)
    sum2 = sum_column(data, col2)

    for res in [sum1, sum2]:
        if "error" in res:
            return res

    if sum2["result"] == 0:
        return {"result": 0}

    # Compute the rate between the two sum
    return {"result": round(sum1["result"] / sum2["result"], 2)}


def sum_groupby_column(data: pd.DataFrame, list_col_gb: List[str], list_col_sum: List[str]) -> dict:
    """ Compute a Series of sums of 'grouped by' values for a list of columns

    Parameters
    ----------
    data: filtered cube with multiple columns
    list_col_gb: list of column names to groupby
    list_col_sum: list of column names to sum after groupby

    Returns
    -------
    dict :
        {"result": <pd.DataFrame>} : DataFrame gathering the grouped by and the summed columns
        or {"error": <reason of error">}
    """

    if not list_col_gb or not list_col_sum:
        return {"error": "no column to group by or to sum"}

    for col in list_col_gb + list_col_sum:
        if col not in data.columns:
            return {"error": "nonexistent column: " + col}

    for col in list_col_sum:
        if data[col].dtypes not in ["int64", "float64"]:
            return {"error": "data with invalid type"}

    gb = data.groupby(list_col_gb)[list_col_sum].sum().reset_index()

    return {"result": gb}


def rate_groupby_column(data: pd.DataFrame, list_col_gb: List[str], col1: str, col2: str) -> dict:
    """ Compute a Series of rates between two groupby columns

    Parameters
    ----------
    data: filtered cube with multiple columns
    list_col_gb: list of column names to groupby
    col1: column name corresponding to the nominator of the rate
    col2: column name corresponding to the denominator of the rate

    Returns
    -------
    dict :
        {"result": <pd.DataFrame>} : DataFrame gathering the grouped by columns and the rate column
        or {"error": <reason of error">}
    """

    gb = sum_groupby_column(data, list_col_gb, [col1, col2])

    if "error" in gb:
        return gb

    # Get only the usefull column (grouped by ones)
    res = gb["result"].reindex(list_col_gb, axis="columns")

    # Add new column to store the rate for every row
    res["rate"] = round(gb["result"][col1] / gb["result"][col2], 2)

    # Get "inf" value when dividing by 0, so replace it with 0
    res["rate"] = res["rate"].replace(np.inf, 0)

    return {"result": res}


def get_col_name(data: pd.DataFrame, col_name: str, default_name: str) -> dict:
    """ Return column name if exist, else the default one

    Parameters
    ----------
    data: filtered cube with multiple columns
    col_name: name of the analysed column
    default_name: name of the default column

    Returns
    -------
    dict :
        {"result": <str: name of column>} or {"error": <reason of error">}
    """

    if col_name in data.columns:
        return col_name

    return default_name


def get_top_n(data: pd.DataFrame, sort_col: str, ascending: bool = True,
              nb: int = None) -> dict:
    """ Get the nb first sorted elements

    Parameters
    ----------
    data: result of other compute operation
    sort_col: the name of the column that will be sorted
    ascending: boolean indicating the sorting direction
    nb: number of the first desired lines of the sort

    Returns
    -------
    dict :
        {"result": <pd.DataFrame>} : DataFrame sorted by `sort_col` column eventually limited to
        the n first lines
        or {"error": <reason of error">}
    """

    if not sort_col:
        return {"error": "no column to sort"}

    if sort_col not in data.columns:
        return {"error": "nonexistent column: " + sort_col}

    sort = data.sort_values(by=sort_col, ascending=ascending)

    if nb:
        return {"result": sort[:nb]}
    return {"result": sort}


def add_all_to_timeline(
        data: pd.DataFrame, list_val: List[str], list_col_gb: List[str], col1: str,
        col_name: str, last_result: pd.DataFrame, col2: str = None
        ) -> dict:
    """
    Add new rows to `last_result` gathering the element values of one groupby column with
    label "ALL"

    Parameters
    ----------
    data: filtered cube with multiple columns
    list_val: list of parameters sent by the front, ex: names of intent
    list_col_gb: column name to groupby
    col1: column name to sum or rate nominator
    col2: column name of rate denominator, optional
    col_name: column name which will be gathered after other column grouped by
    last_result: result of a sum_groupby or rate_groupby which will be enriched with the
    values "ALL" for the `col_groupby` elements

    Returns
    -------
    dict :
        {"result": <pd.DataFrame>} : DataFrame last_result enriched with "ALL" for every
        `col_groupby` columns
        or {"error": <reason of error">}

    Example
    -------
    add_all_to_timeline(df, list_val=["ALL"], list_col_gb=["languages"],
        col1="nb_hab", col_name="countries", last_result=sum_gb
    )
    >>>    languages countries  nb_hab
    0       ENG        UK     350
    1       ENG       USA     700
    2       ESP   Mexique     750
    3       ENG       ALL    1050
    4       ESP       ALL     750
    """

    if "ALL" in list_val:

        if last_result is None:
            return {"error": "last_result is None"}

        # Check if col exists in DataFrames, other columns are checked in next function
        if col_name not in data.columns:
            return {"error": "nonexistent column: " + col_name}

        list_col = list_col_gb + [col_name]
        for col in list_col:
            if col not in last_result.columns:
                return {"error": "nonexistent column: " + col}

        # Compute the new "ALL" rows with only one column to groupby
        if col2:  # then the calcul is a rate
            res = rate_groupby_column(data, list_col_gb, col1, col2)

        else:
            res = sum_groupby_column(data, list_col_gb, [col1])

        if "error" in res:
            return res

        res = res["result"]
        res[col_name] = "ALL"
        return {"result": pd.concat([last_result, res]).reset_index(drop=True)}

    return {"result": last_result}


def filter_line_cube(data: pd.DataFrame, filter_col: str, filter_values: List[str]) -> dict:
    """ Filter object according to some filter values

    Parameters
    ----------
    data: filtered cube with multiple filter_columns
    col: name of the column where the values to be filtered are located
    filter_values: list of values to filter

    Returns
    -------
    dict :
        {"result": <pd.DataFrame>} : DataFrame containing all the row whose column `col` value
        is part of `filter_values`
        or {"error": <reason of error">}
    """

    if filter_col not in data.columns:
        return {"error": "nonexistent column: " + filter_col}

    if filter_values and "ALL" not in filter_values:  # check if list is empty
        return {"result": data[data[filter_col].isin(filter_values)]}

    return {"result": data}


# ################################################
# ############## Specific functions ##############
# ################################################

def remove_small_intent(data: pd.DataFrame) -> dict:
    """Remove all data whose intent begins with 'small-'

    Parameters
    ----------
    data: filtered cube with multiple columns

    Returns
    -------
    pd.Dataframe : the same DataFrame as input but without all the lines where column 'intent'
    value begins whith 'small-'
    """

    if "intent" not in data.columns:
        return {"error": "column 'intent' not existing in data"}

    return {"result": data[~data['intent'].str.startswith('small-')]}


lib_functions = {
    "sum_column": sum_column,
    "rate_column": rate_column,
    "sum_groupby_column": sum_groupby_column,
    "rate_groupby_column": rate_groupby_column,
    "get_col_name": get_col_name,
    "get_top_n": get_top_n,
    "add_all_to_timeline": add_all_to_timeline,
    "filter_line_cube": filter_line_cube
}
