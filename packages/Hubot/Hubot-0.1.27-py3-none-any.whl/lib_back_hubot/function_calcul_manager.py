from typing import Union, List

from lib_back_hubot import lib_functions


def _add_front_param(fct_params: dict, front_params: dict, front_filters: dict) -> dict:
    """Add some parameters choosen by user in the front to initial function parameters

    Parameters
    ----------
    fct_params : dict
        Initial function parameters
    front_params : dict
        key: Name of the parameter in the compute function
        value : Name of the front variable where are the data choosen by the user
    front_filters : dict
        Name of the front variables and their corresponding values choosen by the user

    Example
    -------
    for the function sum_groupby_column(data: pd.DataFrame, list_col_gb: List[str], list_col_sum: List[str])
    - front_params :  {"list_col_gb": "selected_intent"}
    - front_filters:  {"selected_intent": ["sim", "facture"]}

    Returns
    -------
    dict
        Parameters with new data from front
    """
    if front_params:
        for param in front_params:

            if front_params[param] in front_filters:
                fct_params[param] = front_filters[front_params[param]]
            else:
                return {"error": "missing parameter supplied in front_filters: " + front_params[param]}

    return fct_params


def _get_step_function(function: object, calcul_function: dict) -> dict:
    """Get the function object of the step

    Parameters
    ----------
    function : object
        Calcul function
    calcul_function : dict
        All of the available calcul functions

    Returns
    -------
    dict
        Calcul function object or error
    """
    if type(function) is str:
        if function in calcul_function:
            function = calcul_function[function]
        else:
            return {"error": "The function {} is not defined".format(function)}

    return {"result": function}


def _get_step_value(step_params: dict, front_filters: dict, cubes: dict,
                    last_result: object = None, calcul_functions: dict = None) -> dict:
    """Get the result of one step of the KPI compute

    Parameters
    ----------
    step_params : dict
        All the necessary details to get the result step
    front_filters : dict
        Specific values to filter, choosed by the user in the front
    cubes : dict
        List of cubes where are the data to compute
    last_result : object, optional
        Result from the previous step to modify, by default None
    calcul_functions : dict
        Functions from lib and user

    Returns
    -------
    dict
        Value of one step of KPI
    """
    calcul_fct = step_params["function"]
    calcul_params = step_params["basic_params"]
    front_params = step_params["front_params"]  # List of some parameter names of the calc function
    cube_name = step_params["cube"]
    col_last_result = step_params["col_last_result"]

    # Concatenate the `calcul_params` parameters given in the payload and those chosen in the frontend
    calcul_params = _add_front_param(calcul_params, front_params, front_filters)
    if "error" in calcul_params:
        return calcul_params

    calcul_fct = _get_step_function(calcul_fct, calcul_functions)
    if "error" in calcul_fct:
        return calcul_fct
    else:
        calcul_fct = calcul_fct["result"]

    # Set `last_result` to its dedicated parameter
    if last_result is not None and col_last_result is not None:
        calcul_params[col_last_result] = last_result

    # Get the data from the dedicated cube
    if cube_name:
        calcul_params["data"] = cubes[cube_name]

    # Compute the step based on the provided calculation function and the constructed parameters
    try:
        res = calcul_fct(**calcul_params)
    except Exception as err:
        return {"error": str(err)}

    # Then returns the result making sure the function returns the right response format
    if type(res) is dict and ("result" in res or "error" in res):
        return res

    else:
        return {'result': res}


def _get_kpi_value(kpi_params: dict, front_filters: dict, cubes: dict, calcul_functions: dict = None) -> dict:
    """Get the final KPI value for a specific filtered cube after every compute step

    Parameters
    ----------
    kpi_params : dict
        Kpi basic parameters
    front_filters : dict
        Specific values to filter, choosed by the user in the front
    cubes : dict
        All the data to compute divided in many DataFrames
    calcul_functions :
        Functions from lib and user

    Returns
    -------
    dict
        Final KPI value
    """

    list_step = kpi_params["steps"]
    res = None
    last_result = None

    # Execute every compute step to get the final KPI value
    for step in list_step:
        res = _get_step_value(step, front_filters, cubes, last_result, calcul_functions)
        if "error" in res:
            return res

        last_result = res["result"]

    return {"result": res["result"]}


def _get_calcul_functions(lib_functions: dict, external_calcul_functions: dict = None) -> dict:
    """Merge the lib calcul function with optionnal external function from user

    Parameters
    ----------
    lib_functions : dict
        Original calcul functions
    external_calcul_functions : dict, optional
        Additional functions provided by the user, by default None

    Returns
    -------
    dict
        Merged dictionnary of all calcul functions
    """
    calcul_functions = lib_functions.copy()
    if external_calcul_functions:
        calcul_functions.update(external_calcul_functions)

    return calcul_functions


def get_all_kpi(
        kpi_to_calc: List[str], kpi_functions: dict, front_filters: dict, cubes: dict,
        external_calcul_functions: dict = None
     ) -> dict:
    """Compute all the KPI from payload

    Parameters
    ----------
    kpi_to_calc : dict
         Dict of kpi and their parameters
    kpi_functions : dict
        All the necessary parameters and data to compute a KPI
    front_filters : dict
        Specific values to filter, choosed by the user in the front
    cubes : dict
        All the data to compute divided in many DataFrames
    external_calcul_functions : dict, optional
        Additional functions provided by the user, by default None

    Returns
    -------
    dict
        Every result of KPI and optionally its comparison with previous period
    """

    calcul_functions = _get_calcul_functions(lib_functions, external_calcul_functions)

    kpi_values = {}
    for kpi in kpi_to_calc:
        # Get front filters if exist
        kpi_front_filters = front_filters[kpi] if kpi in front_filters else {}

        # Get result of KPI
        try:
            kpi_values[kpi] = _get_kpi_value(kpi_functions[kpi], kpi_front_filters, cubes, calcul_functions)
        except Exception as err:
            kpi_values[kpi] = {"error": str(err)}

    return kpi_values


def compare_two_metrics(res1: Union[int, float], res2: Union[int, float]) -> dict:
    """Get the variation rate between two metrics

    Parameters
    ----------
    res1 : Union[int, float]
        initial value
    res2 : Union[int, float]
        end value

    Returns
    -------
    float
        result of variation rate
    """

    if res1 != 0:
        return {"result": ((res2 - res1) / res1 * 100)}

    return {"result": ""}
