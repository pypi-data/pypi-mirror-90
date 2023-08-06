from typing import List, Callable
from lib_back_hubot import list_cube, check_cubes, complete_filter_cube, convert_filters, \
                            filter_list_of_cubes, need_date_before, get_date_before_filter, \
                            list_cube_containing_date_before

from lib_back_hubot import check_cube_kpi, filter_correct_kpi, compare_two_metrics


from lib_back_hubot import get_all_kpi


DATE_FILTERS = 'dates'
BASE_FILTERS = 'base'


def process_kpi(list_kpi: List[str],
                kpi_functions: dict,
                cube_loader: Callable[[List[str]], dict],
                filters: dict,
                filters_to_cube_colname: dict = {},
                filters_to_cube_values: dict = {},
                front_filters: dict = {},
                date_format: str = "%d-%m-%Y",
                external_calcul_functions: dict = None) -> dict:

    # Get all the valid KPI to compute
    valid_kpi, error_kpi = filter_correct_kpi(list_kpi, kpi_functions)

    # Get all needed cube and load them
    cube_names, metric_cube_names, kpi_cube_names = list_cube(valid_kpi, kpi_functions)
    loaded_cubes = cube_loader(cube_names)

    # Get only the KPI whose cubes have been loaded correctly
    valid_cubes, missing_cube, invalid_cube = check_cubes(cube_names, loaded_cubes)
    valid_kpi, missing_cube_kpi = check_cube_kpi(valid_kpi, valid_cubes, kpi_cube_names)

    # Filter data
    dates_filters = filters[DATE_FILTERS]
    data_filters = filters[BASE_FILTERS]
    filters_to_cube_colname, filters_to_cube_values = complete_filter_cube(
        data_filters, filters_to_cube_colname, filters_to_cube_values
    )
    data_filters = convert_filters(
        data_filters, filters_to_cube_colname, filters_to_cube_values
    )

    filtered_cubes = filter_list_of_cubes(
        valid_cubes, loaded_cubes, dates_filters, data_filters, date_format
    )

    # Get kpi result for all type of KPI
    result_kpi = get_all_kpi(valid_kpi, kpi_functions, front_filters, filtered_cubes, external_calcul_functions)

    # Get comparison for metric type KPI
    if need_date_before(metric_cube_names, dates_filters):

        metric_cube = [cube for cube in metric_cube_names if cube in valid_cubes]
        metric_kpi = [kpi for kpi in valid_kpi if kpi_functions[kpi]["type"] == "metric"]

        dates_before_filters = get_date_before_filter(dates_filters, date_format)
        date_before_cube_list = list_cube_containing_date_before(
            metric_cube, loaded_cubes, dates_before_filters, date_format
        )
        valide_date_before_kpi, missing_cube_before_kpi = check_cube_kpi(
            metric_kpi, date_before_cube_list, kpi_cube_names
        )

        period_before_cube = filter_list_of_cubes(
            date_before_cube_list, loaded_cubes, dates_before_filters, data_filters, date_format
        )

        comparison_result = get_all_kpi(
            metric_kpi, kpi_functions, front_filters, period_before_cube, external_calcul_functions
        )

        comparison_kpi = {
            kpi: comparison_result[kpi] for kpi in comparison_result if "error" not in comparison_result[kpi]
        }

        for kpi in comparison_kpi:
            result = result_kpi[kpi]["result"]
            comparison = comparison_result[kpi]["result"]

            result_kpi[kpi]['comparaison'] = compare_two_metrics(result, comparison)

    for kpi in error_kpi:
        result_kpi[kpi] = error_kpi[kpi]

    for kpi in missing_cube_kpi:
        result_kpi[kpi] = missing_cube_kpi[kpi]

    return result_kpi
