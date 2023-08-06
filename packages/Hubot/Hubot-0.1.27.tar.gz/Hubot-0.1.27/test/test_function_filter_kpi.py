import pytest

from test.helper import load_file
from lib_back_hubot import _check_existent_kpi, _check_params, _check_validity_kpi, filter_correct_kpi, \
                            check_cube_kpi


@pytest.mark.parametrize("directory, filename", [
    ("check_existent_kpi", "nominal"),
    ("check_existent_kpi", "missing_kpi")
])
def test_check_existent_kpi(directory, filename):

    payload = load_file('payloads', 'function_filter_kpi', directory, filename)
    result = _check_existent_kpi(payload["kpi_to_calc"], payload["kpi_functions"])

    expectation = load_file('expectation', 'function_filter_kpi', directory, filename)["result"]

    assert result == (expectation[0], expectation[1])


@pytest.mark.parametrize("directory, filename", [
    ("check_params", "nominal"),
    ("check_params", "no_required_param"),
    ("check_params", "wrong_type"),
    ("check_params", "no_dict")
])
def test_check_params(directory, filename):
    payload = load_file('payloads', 'function_filter_kpi', directory, filename)
    result = _check_params(payload["valid_params"], payload["object_params"], payload["index"])

    expectation = load_file('expectation', 'function_filter_kpi', directory, filename)

    assert result == expectation


@pytest.mark.parametrize("directory, filename", [
    ("check_validity_kpi", "nominal"),
    ("check_validity_kpi", "missing_parameter"),
    ("check_validity_kpi", "wrong_value_param")
])
def test_check_validity_kpi(directory, filename):
    payload = load_file('payloads', 'function_filter_kpi', directory, filename)
    result = _check_validity_kpi(payload["existent_kpi"], payload["kpi_functions"])

    expectation = load_file('expectation', 'function_filter_kpi', directory, filename)["result"]

    assert result == (expectation[0], expectation[1])


@pytest.mark.parametrize("directory, filename", [
    ("filter_correct_kpi", "nominal"),
    ("filter_correct_kpi", "inexistent_kpi"),
    ("filter_correct_kpi", "wrong_type_inexistent_kpi")
])
def test_filter_correct_kpi(directory, filename):
    payload = load_file('payloads', 'function_filter_kpi', directory, filename)
    result = filter_correct_kpi(payload["list_kpi"], payload["kpi_functions"])

    expectation = load_file('expectation', 'function_filter_kpi', directory, filename)["result"]

    assert result == (expectation[0], expectation[1])


@pytest.mark.parametrize("directory, filename", [
    ("check_cube_kpi", "nominal"),
    ("check_cube_kpi", "error_cube")
])
def test_check_cube_kpi(directory, filename):
    payload = load_file('payloads', 'function_filter_kpi', directory, filename)
    result = check_cube_kpi(payload["valid_kpi"], payload["valid_cube"], payload["kpi_cube"])

    expectation = load_file('expectation', 'function_filter_kpi', directory, filename)["result"]
    assert result == (expectation[0], expectation[1])
