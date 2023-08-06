from datetime import datetime
import warnings
from typing import List, Tuple

import pandas as pd


def _set_pd_timestamp(date_str: str, set_timestamp: datetime, format: str, tz) -> datetime:
    """Create a pd.datatime from a str date

    Parameters
    ----------
    date_str : str
    set_timestamp : pd.datetime
        the default timestamp if date_str is none
    set_timestamp : str
        the date_str format
    tz :
        the timezone use by pandas

    Returns
    -------
    pd.datetime
    """
    if date_str is None:
        date_str = set_timestamp
    else:
        date_str = datetime.strptime(date_str, format).replace(tzinfo=tz)
    return date_str


def _date_to_pd_datetime(from_date: str, to_date: str, tz, format: str) -> Tuple[datetime, datetime]:
    """Convert from_date and to_date to pandas datetime format

    Parameters
    ----------
    from_date : str

    to_date : str

    tz :
        the timezone use for the datetime
    format : str
        the format of the datetime

    Returns
    -------
    Tuple[pd.datetime, pd.datetime]
        the new from_date and to_date
    """
    from_date = _set_pd_timestamp(from_date, pd.Timestamp.min, format, tz)
    to_date = _set_pd_timestamp(to_date, pd.Timestamp.max, format, tz)

    if from_date > to_date:
        from_date, to_date = to_date, from_date

    return from_date, to_date


def _filter_cube_date(cube: pd.DataFrame, date_filter: dict, format: str) -> pd.DataFrame:
    """Filter the cube with the selected date and return it

    Parameters
    ----------
    cube : pd.DataFrame
        the cube of data
    date_filter : dict
        a dictionnary containing the date filter
    format : str, optional
        the format of the date present in the date filter, must be accepted by
        panda.to_datetime, by default "%d-%m-%Y"

    Returns
    -------
    pd.DataFrame
        the filtered cube
    """
    if date_filter['mode'] == "ALL":
        return cube
    else:
        tz = cube['tstamp'].dt.tz
        from_date, to_date = _date_to_pd_datetime(date_filter['from'], date_filter['to'], tz, format)
        data = cube[cube['tstamp'].between(from_date, to_date, inclusive=True)]
    return data


def _apply_filter(filters: dict, cube: pd.DataFrame) -> pd.DataFrame:
    """  Filter the cube with the accepted value in filters and return it

    Parameters
    ----------
    filters : dict
        list of accepted value for each filtered column of the cube
    cube : pd.DataFrame
        the cube to filter

    Returns
    -------
    pd.DataFrame
        the filtered cube
    """
    for data_filter in filters:
        if data_filter in cube.columns:
            cube = cube[cube[data_filter].isin(filters[data_filter])]
    return cube


def _cube_contain_date_before(cube: pd.DataFrame, date_before_filter: dict, format: str) -> bool:

    """Test if the cube contain the date of a date filter,
    use to know if it's relevant to filter the date before for this cube

    Parameters
    ----------
    cube : pd.DataFrame
        the data cube
    date_before_filter : dict
        the original filter
    format : str
        the date format use

    Returns
    -------
    bool
        true if the cube contain the date, false otherwise
    """
    min_ok = cube['tstamp'].min() <= datetime.strptime(date_before_filter['from'], format)
    max_ok = cube['tstamp'].max() >= datetime.strptime(date_before_filter['to'], format)

    return min_ok and max_ok


def list_cube(list_kpi: list, kpi_functions: dict) -> Tuple[set, set]:
    """List the name of the cubes needed by all KPI, by metric KPI and per each KPI

    Parameters
    ----------
    list_kpi : list
        All the KPI we want to compute
    kpi_functions : dict
        Dictionnary containing all the required parameters to compute each KPI

    Returns
    -------
    Tuple[set, set, dict]
        The first set contains all the name of the cubes needed by all KPI
        The second set only contains the name of the cubes used by metrics KPI
            (for these KPI we need to filter the cube twice :
            - One time for the selected dates
            - One time for the last period dates)
        The dictionnary associate each KPI and the names of the cubes it needs
    """

    cube_name = []
    cube_metric_name = []
    kpi_cube_needed = {}

    for kpi in list_kpi:

        kpi_cube_needed[kpi] = set([None])

        for step in kpi_functions[kpi]["steps"]:
            if kpi_functions[kpi]["type"] == 'metric':
                cube_metric_name.append(step["cube"])

            cube_name.append(step["cube"])
            kpi_cube_needed[kpi].add(step["cube"])

        # Sometimes steps doesn't need cube, None is written instead so remove it
        kpi_cube_needed[kpi].remove(None)
        kpi_cube_needed[kpi] = list(kpi_cube_needed[kpi])

    # Remove None value
    cube_name = set(filter(None, cube_name))
    cube_metric_name = set(filter(None, cube_metric_name))

    return cube_name, cube_metric_name, kpi_cube_needed


def check_cubes(list_cube: List[str], cube_data: dict) -> Tuple[bool, list, list]:
    """Determines the names of the correctly loaded and valid cubes, missing cubes and invalid cubes

    Parameters
    ----------
    list_cube : List[str]
        list of the names of the needed cubes
    cube_data : dict
        all the cubes loaded

    Returns
    -------
    Tuple[list, list, list]
        - List of the names of the cubes that have been loaded correctly and whose data is valid
        - List of the names of missing cubes
        - List of the names of invalid cubes
    """
    valid = []
    missing = []
    invalid = []

    for cube in list_cube:

        if cube in cube_data:
            if type(cube_data[cube]) is not pd.DataFrame:
                invalid.append(cube)
            # Check if type of tstamp data is datetime
            elif not pd.core.dtypes.common.is_datetime64_dtype(cube_data[cube]["tstamp"]):
                invalid.append(cube)
            else:
                valid.append(cube)

        else:
            missing.append(cube)

    return valid, missing, invalid


def complete_filter_cube(filters: dict, filter_to_cube_col: dict, filter_to_cube_values: dict) -> Tuple[dict, dict]:
    """Complete `filter_to_cube_col` and `filter_to_cube_values` with
    the filters if there is missing values in them

    Parameters
    ----------
    filters : dict
        the filters use to filter the cubes
    filter_to_cube_col : dict
        dictionnary to transform a filter key to a cube column name
    filter_to_cube_values : dict
        dictionnary to transform a filter value to a cube column value

    Parameter example
    -----------------
    - Input :
    filters : {
        device : {mobile': True, 'desktop' : False},
        country : {'France' : True, 'Germany' : False}
    }
    filter_to_cube_col : {'device' : 'technology'}
    filter_to_cube_value : {'device' : {'mobile' : 'smartphone'}}

    - Output :
    filter_to_cube_col : {device' : 'technology', 'country' : 'country'}
    filter_to_cube_value : {
        'device' : {'mobile' : 'smartphone', 'desktop' : 'desktop'}
        'country' : {'France' : 'France','Germany' : 'Germany'}

    Returns
    -------
    Tuple[dict, dict]
        the new filter_to_cube_col and filter_to_cube_values
    """
    for filter_name in filters:
        if filter_name not in filter_to_cube_col:
            filter_to_cube_col[filter_name] = filter_name

        if filter_name not in filter_to_cube_values:
            filter_to_cube_values[filter_name] = {}

        for filter_val in filters[filter_name]:
            if filter_val not in filter_to_cube_values[filter_name]:
                filter_to_cube_values[filter_name][filter_val] = filter_val

    return filter_to_cube_col, filter_to_cube_values


def convert_filters(filters: dict, filter_to_cube_col: dict, filter_to_cube_values: dict) -> dict:
    """ For each filter, store in the dictionnary the list of accepted value
    at the key corresponding to the cube column name.

    Parameters
    ----------
    filters : dict
        The filters use for the cube
    filter_to_cube_col : dict
        for each filter key the assiciated cube column name
    filter_to_cube_values : dict
        for each filter value the associated cube column value

    Returns
    -------
    dict
        Association of filters and their accepted values corresponding to cube column name
    """
    new_filters = {}

    for data_filter in filters:
        accepted_values = []
        for key, val in filters[data_filter].items():
            if val:
                accepted_values.append(filter_to_cube_values[data_filter][key])

        new_filters[filter_to_cube_col[data_filter]] = accepted_values
    return new_filters


def filter_list_of_cubes(cube_list: list, cube_data: dict,
                         dates_filters: dict, data_filters: dict,
                         date_format: str) -> dict:
    """filter each cube of cube_list

    Parameters
    ----------
    cube_list : list
        the list of all cube needed
    cube_data : dict
        dictionnary containing all cubes, with their name as the key
    dates_filters : dict
        the date filters
    data_filters : dict
        the data filters (accepted value for some column of each cube)
    date_format : str
        the date format

    Returns
    -------
    dict
        a dictionnary of all filtered cube
    """
    result = {}
    for cube in cube_list:
        result[cube] = _filter_cube_date(cube_data[cube], dates_filters, date_format)
        result[cube] = _apply_filter(data_filters, result[cube])

    return result


def need_date_before(cube_metric: list, date_filters: dict) -> bool:
    """Check if we need to filter metric cube with the date before

    Parameters
    ----------
    cube_metric : list
        list of all cube needed to calculate metrics
    date_filters : dict
        the date filters

    Returns
    -------
    bool
        true if it's needed, false otherwise
    """
    return len(cube_metric) > 0 and date_filters['mode'] != "ALL"


def get_date_before_filter(date_filters: dict, format: str) -> dict:
    """Transform the input date filter to return a date filter
    corresponding to the equivalent previous period

    Parameters
    ----------
    date_filters : dict
        the original date filter

    Returns
    -------
    dict
        the date filter for the previous period
    """
    ts_from = pd.to_datetime(date_filters['from'], format=format)
    ts_to = pd.to_datetime(date_filters['to'], format=format)

    if ts_from > ts_to:
        ts_from, ts_to = ts_to, ts_from

    delta = (ts_to - ts_from) + pd.Timedelta(days=1)

    ts_from_bis = ts_from - delta
    ts_to_bis = ts_to - delta

    result = date_filters.copy()
    result['to'] = ts_to_bis.strftime(format)
    result['from'] = ts_from_bis.strftime(format)

    return result


def list_cube_containing_date_before(cube_list: list, cube_data: dict,
                                     dates_before_filters: dict, format: str) -> list:
    """For each cube, check if the dates in date_before_filters are present in the cube,
    if they are all there, add it to the return list. Return the list when all cubes are checked

    Parameters
    ----------
    cube_list : list
        all the cube name we want to test
    cube_data : dict
        {<cube name> : <cube as a dataframe>}
    dates_before_filters : dict
        the filters containing the dates
    format : str
        the date format use

    Returns
    -------
    list
        list of cube name which contain the date
    """
    result = []
    if dates_before_filters['mode'] != "ALL":
        for cube in cube_list:
            if _cube_contain_date_before(cube_data[cube], dates_before_filters, format):
                result.append(cube)

    return result


def apply_scale_to_cube(cube: pd.DataFrame, scale: str) -> pd.DataFrame:
    """Transform the tstamp of the cube to the correct scale

    Parameters
    ----------
    cube : pd.DataFrame
    scale : str
        can be WEEK - MONTH - DAY
    Returns
    -------
    pd.DataFrame
        [description]
    """

    if scale == 'WEEK':
        cube['tstamp'] = cube['tstamp'].dt.to_period('W').dt.to_timestamp()
        return cube
    elif scale == 'MONTH':
        cube['tstamp'] = cube['tstamp'].dt.to_period('M').dt.to_timestamp()
        return cube
    elif scale == 'DAY':
        return cube
    else:
        msg = 'SCALE ignore, wrong scale format '+scale
        msg += ' - accepted format : DAY WEEK MONTH'
        warnings.warn(msg, Warning)
        return cube
