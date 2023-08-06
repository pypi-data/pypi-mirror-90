from typing import List, Tuple


DICT_TYPE = {
    "str": str,
    "int": int,
    "float": float,
    "dict": dict,
    "list": list
}


def _check_existent_kpi(kpi_to_calc: List[str], kpi_functions: dict):
    """ Check if the wanted KPIs exist in a predefined list of known KPI

    Parameters
    ----------
    kpi_to_calc : List[str]
        KPI names we want to compute
    kpi_functions : dict
        All the necessary parameters and data to compute a KPI

    Returns
    -------
        Tuple[List[str], List[str]]
        First a list of all the existing KPI, then a list of all the inexisting KPI
    """
    nonexistent_kpi = []
    existent_kpi = []

    for kpi in kpi_to_calc:
        if kpi not in kpi_functions:
            nonexistent_kpi.append(kpi)
        else:
            existent_kpi.append(kpi)

    return existent_kpi, nonexistent_kpi


def _check_params(valid_params: dict, object_params: dict, index: int):
    """ Check the type and presence (if necessary) of data for multiple parameters

    Parameters
    ----------
    valid_params : dict
        Set of parameters, their necessity and their type
    object_params : dict
        Set of parameters whose data are to be verified
    index : int
        Step number

    Returns
    -------
    List[str]
        All errors found
    """

    errors = []

    if type(object_params) is not dict:
        return ["Parameters object is not a dict"]

    if len(object_params) != len(valid_params) or not all(p in object_params for p in valid_params):
        errors.append("Missing kpi parameters: {}".format(list(valid_params.keys())))

    else:
        for param in valid_params:

            required = valid_params[param]["is_required"]
            param_type = type(object_params[param])
            valid_type = DICT_TYPE[valid_params[param]["type"]]

            if required and object_params[param] is None:
                errors.append("Step {} - Required parameter {} is None".format(index, param))

            elif required and param_type is not valid_type:
                errors.append("Step {} - {} parameter is not a {}".format(index, param, valid_params[param]["type"]))

            elif not required and object_params[param] is not None and param_type is not valid_type:
                errors.append("Step {} - {} parameter is not a {}".format(index, param, valid_params[param]["type"]))

    return errors


def _check_validity_kpi(existent_kpi: List[str], kpi_functions: dict):
    """Check the validity of a set of KPIs

    Parameters
    ----------
    existent_kpi : List[str]
        Set of KPI we want to check validity
    kpi_functions : dict
        All the necessary parameters and data to compute a KPI

    Returns
    -------
    Tuple[List[str], dict]
        First a list of all the valid KPI, then a dict of all the invalid KPI wth their errors
    """

    valid_kpi = []
    invalid_kpi = {}

    initial_param = {
        "type": {"is_required": True, "type": "str"},
        "info": {"is_required": False, "type": "dict"},
        "steps": {"is_required": True, "type": "list"}
    }

    step_params = {
        "function": {"is_required": True, "type": "str"},
        "cube": {"is_required": False, "type": "str"},
        "basic_params": {"is_required": False, "type": "dict"},
        "front_params": {"is_required": False, "type": "dict"},
        "col_last_result": {"is_required": False, "type": "str"}
    }

    for kpi in existent_kpi:
        errors = []
        errors += _check_params(initial_param, kpi_functions[kpi], "Initial parameters")

        if "steps" in kpi_functions[kpi]:
            for idx, step in enumerate(kpi_functions[kpi]["steps"]):
                errors += _check_params(step_params, step, idx + 1)

        if len(errors) > 0:
            invalid_kpi[kpi] = errors
        else:
            valid_kpi.append(kpi)

    return valid_kpi, invalid_kpi


def filter_correct_kpi(list_kpi: List[str], kpi_functions: dict):
    """ Get all the existing and valid KPIs, get error for the others

    Parameters
    ----------
    list_kpi : List[str]
        KPI names we want to compute
    kpi_functions : dict
        All the necessary parameters and data to compute a KPI

    Returns
    -------
    Tuple[List[str], dict]
        Get the correct KPI, and the wrong KPIs with their corresponding error
    """
    error_kpi = {}

    # Check if KPIs exist
    existent_kpi, nonexistent_kpi = _check_existent_kpi(list_kpi, kpi_functions)

    for kpi in nonexistent_kpi:
        error_kpi[kpi] = {"error": "Nonexistent kpi in kpi_functions"}

    # Check if KPIs are valid
    valid_kpi, invalid_kpi = _check_validity_kpi(existent_kpi, kpi_functions)
    for kpi in invalid_kpi:
        error_kpi[kpi] = {"error": invalid_kpi[kpi]}

    return valid_kpi, error_kpi


def check_cube_kpi(valid_kpi: List[str], valid_cubes: List[str], kpi_cube: dict) -> Tuple[List[str], dict]:

    """for each valid kpi, check if the cubes needed to calculate it
       are in valid_cubes

    Parameters
    ----------
    valid_kpi : List[str]
        all valid kpi
    valid_cubes : List[str]
        all valid cube
    kpi_cube : dict
        dictionnary containing the necessary cubes for each kpi

    Returns
    -------
    Tuple[list[str], dict]
        return the new list of valid kpi and a dictionnary containing the error of other kpi
    """
    error = {}
    new_valid_kpi = []

    for kpi in kpi_cube:

        missing = [cube for cube in kpi_cube[kpi] if cube not in valid_cubes]
        if len(missing) > 0:
            error[kpi] = {"error": "cube not correctly loaded: "+'-'.join(missing)}
        else:
            new_valid_kpi.append(kpi)

    return new_valid_kpi, error
