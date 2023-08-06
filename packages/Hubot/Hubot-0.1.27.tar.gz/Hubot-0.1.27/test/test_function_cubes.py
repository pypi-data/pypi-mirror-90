import pandas as pd
import pytest

from test.helper import load_file

from lib_back_hubot import (_apply_filter, _cube_contain_date_before,
                            _filter_cube_date, apply_scale_to_cube,
                            check_cubes, complete_filter_cube, convert_filters,
                            filter_list_of_cubes, get_date_before_filter,
                            list_cube, list_cube_containing_date_before,
                            need_date_before)


@pytest.mark.parametrize("directory, filename", [
    ("list_cube", "list_cube_nominal"),
    ("list_cube", "list_cube_none_cube_name")
    ])
def test_list_cube_nominal(directory, filename):
    payload = load_file('payloads', 'function_cubes', directory, filename)
    result = list_cube(payload['list_kpi'], payload['dico_function'])
    result = list(result)

    result[0] = list(result[0])
    result[0].sort()
    result[1] = list(result[1])
    result[1].sort()
    for kpi in result[2]:
        result[2][kpi].sort()

    expectation = load_file('expectation', 'function_cubes', directory, filename)["result"]
    expectation[0].sort()
    expectation[1].sort()

    assert (result[0], result[1], result[2]) == (expectation[0], expectation[1], expectation[2])


@pytest.mark.parametrize("directory, filename", [
    ("check_cubes", "nominal")
])
def test_check_cubes_nominal(directory, filename):
    payload = load_file('payloads', 'function_cubes', directory, filename)

    cube_data = {}
    for cube in payload["cube_data"]:
        data = payload["cube_data"][cube]
        cube_data[cube] = pd.DataFrame(data)
        cube_data[cube]["tstamp"] = pd.to_datetime(data["tstamp"], format="%d-%m-%Y")

    result = check_cubes(payload["list_cube"], cube_data)
    expectation = load_file('expectation', 'function_cubes', directory, filename)["result"]

    assert result == (expectation[0], expectation[1], expectation[2])


@pytest.mark.parametrize("directory, filename", [
    ("check_cubes", "wrong_type")
])
def test_check_cubes_wrong_type(directory, filename):
    payload = load_file('payloads', 'function_cubes', directory, filename)
    result = check_cubes(payload["list_cube"], payload["cube_data"])

    expectation = load_file('expectation', 'function_cubes', directory, filename)["result"]
    assert result == (expectation[0], expectation[1], expectation[2])


@pytest.mark.parametrize("directory, filename", [
    ("check_cubes", "no_timestamp")
])
def test_check_cubes_no_timestamp(directory, filename):
    payload = load_file('payloads', 'function_cubes', directory, filename)

    cube_data = {}
    for cube in payload["cube_data"]:
        data = payload["cube_data"][cube]
        cube_data[cube] = pd.DataFrame(data)

    result = check_cubes(payload["list_cube"], cube_data)
    expectation = load_file('expectation', 'function_cubes', directory, filename)["result"]

    assert result == (expectation[0], expectation[1], expectation[2])


@pytest.mark.parametrize("directory, filename", [
    ("filter_cube_date", "nominal"),
    ("filter_cube_date", "nominal_2"),
    ("filter_cube_date", "nominal_3"),
    ("filter_cube_date", "nominal_4")])
def test_filter_cube_date(directory, filename):
    payload = load_file('payloads', 'function_cubes', directory, filename)
    expectation = load_file('expectation', 'function_cubes', directory, filename)
    data = pd.DataFrame(payload["data"])
    data["tstamp"] = pd.to_datetime(data["tstamp"], format="%d-%m-%Y")

    expectation = pd.DataFrame(expectation)
    expectation["tstamp"] = pd.to_datetime(expectation["tstamp"],
                                           format="%d-%m-%Y")

    result = _filter_cube_date(data, payload["filtres"], "%d-%m-%Y")
    pd.testing.assert_frame_equal(result, expectation)


@pytest.mark.parametrize("directory, filename", [("convert_filters", "nominal")])
def test_convert_filters(directory, filename):
    payload = load_file('payloads', 'function_cubes', directory, filename)
    expectation = load_file('expectation', 'function_cubes', directory, filename)

    result = convert_filters(**payload)
    assert result == expectation


@pytest.mark.parametrize("directory, filename", [
    ("apply_filter", "nominal"),
    ("apply_filter", "missing_col")])
def test_apply_filter(directory, filename):
    payload = load_file('payloads', 'function_cubes', directory, filename)
    expectation = load_file('expectation', 'function_cubes', directory, filename)

    expectation = pd.DataFrame(expectation).reset_index(drop=True)
    data = pd.DataFrame(payload['data'])
    result = _apply_filter(payload['filters'], data).reset_index(drop=True)

    pd.testing.assert_frame_equal(result, expectation)


@pytest.mark.parametrize("directory, filename", [
    ("need_date_before", "nominal"),
    ("need_date_before", "nominal_2")])
def test_need_date_before(directory, filename):
    payload = load_file('payloads', 'function_cubes', directory, filename)
    expectation = load_file('expectation', 'function_cubes', directory, filename)

    assert need_date_before(**payload) == expectation


@pytest.mark.parametrize("directory, filename", [
    ("get_date_before_filter", "nominal"),
    ("get_date_before_filter", "date_inverse")])
def test_get_date_before_filter(directory, filename):
    payload = load_file('payloads', 'function_cubes', directory, filename)
    expectation = load_file('expectation', 'function_cubes', directory, filename)

    assert get_date_before_filter(**payload) == expectation


@pytest.mark.parametrize("directory, filename", [
    ("cube_contain_date_before", "nominal"),
    ("cube_contain_date_before", "nominal_2"),
    ("cube_contain_date_before", "nominal_3")])
def test_cube_contain_date_before(directory, filename):
    payload = load_file('payloads', 'function_cubes', directory, filename)
    expectation = load_file('expectation', 'function_cubes', directory, filename)

    data = pd.DataFrame(payload['data'])
    data["tstamp"] = pd.to_datetime(data["tstamp"], format="%d-%m-%Y")
    filters_date_before = payload['filters']

    assert _cube_contain_date_before(data, filters_date_before, format="%d-%m-%Y") == expectation


@pytest.mark.parametrize("directory, filename", [
    ("complete_filter_cube", "nominal")])
def test_complete_filter_cube(directory, filename):
    payload = load_file('payloads', 'function_cubes', directory, filename)
    expectation = load_file('expectation', 'function_cubes', directory, filename)

    assert complete_filter_cube(**payload) == (expectation['filter_to_cube_col'], expectation['filter_to_cube_values'])


@pytest.mark.parametrize("directory, filename", [
    ("list_cube_containing_date_before", "nominal"),
    ("list_cube_containing_date_before", "mode_all"),
    ("list_cube_containing_date_before", "missing_date")])
def test_list_cube_containing_date_before(directory, filename):
    payload = load_file('payloads', 'function_cubes', directory, filename)
    expectation = load_file('expectation', 'function_cubes', directory, filename)

    for k in payload["cube_data"]:
        df = pd.DataFrame(payload["cube_data"][k])
        df["tstamp"] = pd.to_datetime(df["tstamp"], format="%d-%m-%Y")
        payload["cube_data"][k] = df

    assert list_cube_containing_date_before(**payload) == expectation


@pytest.mark.parametrize("directory, filename", [
    ("filter_list_of_cubes", "nominal"),
    ("filter_list_of_cubes", "nominal_2")])
def test_filter_list_of_cubes(directory, filename):
    payload = load_file('payloads', 'function_cubes', directory, filename)
    expectation = load_file('expectation', 'function_cubes', directory, filename)

    for k in payload["cube_data"]:
        df = pd.DataFrame(payload["cube_data"][k])
        df['tstamp'] = pd.to_datetime(df["tstamp"], format="%d-%m-%Y")
        payload["cube_data"][k] = df

    for k in expectation:
        df = pd.DataFrame(expectation[k])
        df['tstamp'] = pd.to_datetime(df["tstamp"], format="%d-%m-%Y")
        expectation[k] = df

    result = filter_list_of_cubes(**payload)
    for k in expectation:
        tmp_res = result[k].reset_index(drop=True)
        tmp_exp = expectation[k].reset_index(drop=True)
        pd.testing.assert_frame_equal(tmp_res, tmp_exp)


@pytest.mark.parametrize("directory, filename", [
    ("apply_scale_to_cube", "days"),
    ("apply_scale_to_cube", "week"),
    ("apply_scale_to_cube", "month"),
    ("apply_scale_to_cube", "wrong_format")])
def test_apply_scale_to_cube(directory, filename):
    payload = load_file('payloads', 'function_cubes', directory, filename)
    expectation = load_file('expectation', 'function_cubes', directory, filename)

    df = pd.DataFrame(payload['cube'])
    df['tstamp'] = pd.to_datetime(df["tstamp"], format="%d-%m-%Y")
    payload['cube'] = df

    result = apply_scale_to_cube(**payload)
    result = result['tstamp'].dt.strftime("%d-%m-%Y").values.tolist()

    assert result == expectation
