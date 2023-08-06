import pandas as pd
import pytest

from test.helper import load_file, _sum, _substract

from lib_back_hubot import (_add_front_param, _get_calcul_functions,
                            _get_kpi_value, _get_step_function,
                            _get_step_value, compare_two_metrics, get_all_kpi,
                            lib_functions)


@pytest.mark.parametrize("directory, filename", [
    ("add_front_param", "nominal"),
    ("add_front_param", "missing_parameter")
])
def test_add_front_param(directory, filename):
    payload = load_file('payloads', 'function_calcul_manager', directory, filename)
    expectation = load_file('expectation', 'function_calcul_manager', directory, filename)

    params = _add_front_param(**payload)

    assert params == expectation


def test_get_step_function_nominal():
    calcul_functions = {"_sum": _sum}
    result = _get_step_function("_sum", calcul_functions)

    assert result == {"result": _sum}


def test_gest_step_function_nonexisting():
    calcul_functions = {"_sum": _sum}
    result = _get_step_function("_substract", calcul_functions)

    assert result == {"error": "The function _substract is not defined"}


@pytest.mark.parametrize("directory, filename", [
    ("get_step_value", "nominal"),
    ("get_step_value", "missing_front_param"),
    ("get_step_value", "missing_function_param"),
])
def test_get_step_value(directory, filename):
    payload = load_file('payloads', 'function_calcul_manager', directory, filename)
    expectation = load_file('expectation', 'function_calcul_manager', directory, filename)

    payload['step_params']['function'] = _sum
    step_result = _get_step_value(**payload)

    assert step_result == expectation


@pytest.mark.parametrize("directory, filename", [
    ("get_step_value_str_fct", "nominal"),
])
def test_get_step_value_str_fct(directory, filename):
    payload = load_file('payloads', 'function_calcul_manager', directory, filename)
    expectation = load_file('expectation', 'function_calcul_manager', directory, filename)["result"]["result"]

    cubes = {"cube1": pd.DataFrame({'col1': pd.Series([1, 2])})}
    payload["cubes"] = cubes
    payload["calcul_functions"] = lib_functions

    result = _get_step_value(**payload)["result"]

    assert result == expectation


@pytest.mark.parametrize("directory, filename", [
    ("get_kpi_value", "nominal"),
    ("get_kpi_value", "nominal_front_param"),
    ("get_kpi_value", "missing_front_param")
])
def test_get_kpi_value(directory, filename):
    payload = load_file('payloads', 'function_calcul_manager', directory, filename)
    expectation = load_file('expectation', 'function_calcul_manager', directory, filename)

    payload['kpi_params']["steps"][0]['function'] = _sum
    payload['kpi_params']["steps"][1]['function'] = _sum

    value = _get_kpi_value(**payload)

    assert value == expectation


def test_get_calcul_functions():
    lib_functions = {"sum": _sum}
    external_calcul_functions = {"substract": _substract}

    result = _get_calcul_functions(lib_functions, external_calcul_functions)

    assert result == {"sum": _sum, "substract": _substract}


def test_get_calcul_functions_no_external():
    lib_functions = {"sum": _sum, "substract": _substract}
    result = _get_calcul_functions(lib_functions)

    assert result == {"sum": _sum, "substract": _substract}


@pytest.mark.parametrize("directory, filename", [
    ("get_all_kpi", "nominal"),
    ("get_all_kpi", "missing_front_param")
])
def test_get_all_kpi(directory, filename):
    payload = load_file('payloads', 'function_calcul_manager', directory, filename)
    expectation = load_file('expectation', 'function_calcul_manager', directory, filename)

    for kpi in payload["kpi_functions"]:
        for step in payload['kpi_functions'][kpi]["steps"]:
            step['function'] = _sum

    all_kpi = get_all_kpi(**payload)

    assert all_kpi == expectation


@pytest.mark.parametrize("directory, filename", [
    ("get_all_kpi", "external_function")
])
def test_get_all_kpi_external_function(directory, filename):
    payload = load_file('payloads', 'function_calcul_manager', directory, filename)
    expectation = load_file('expectation', 'function_calcul_manager', directory, filename)["result"]

    payload["external_calcul_functions"] = {"_sum": _sum}
    result = get_all_kpi(**payload)

    assert result == expectation


@pytest.mark.parametrize("directory, filename", [
    ("compare_two_metrics", "nominal"),
])
def test_compare_two_metrics(directory, filename):
    payload = load_file('payloads', 'function_calcul_manager', directory, filename)
    expectation = load_file('expectation', 'function_calcul_manager', directory, filename)

    params = compare_two_metrics(**payload)

    assert params == expectation
