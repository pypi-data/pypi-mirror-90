import numpy as np
import pandas as pd
from pandas._testing import assert_frame_equal

from lib_back_hubot.function_calcul import sum_column, rate_column, sum_groupby_column,\
    rate_groupby_column, get_col_name, get_top_n, add_all_to_timeline, filter_line_cube, \
    remove_small_intent


# ###################################################
# ############## Function sum_column() ##############
# ###################################################


def test_sum_column_valid():
    """ Test correct result with valid data"""

    df = pd.DataFrame({'col1': pd.Series([1, 2])})
    sum_col = sum_column(df, 'col1')

    assert sum_col["result"] == 3


def test_sum_column_nan_value():
    """ Test correct result with NaN value in column """

    df = pd.DataFrame({'col1': pd.Series([1, np.nan, 4])})
    sum_col = sum_column(df, 'col1')

    assert sum_col["result"] == 5


def test_sum_column_empty_column():
    """ Test null result with empty column """

    df = pd.DataFrame({'col1': pd.Series([], dtype="float64")})
    sum_col = sum_column(df, 'col1')

    assert sum_col["result"] == 0


def test_sum_column_full_nan():
    """ Test null result with empty column """

    df = pd.DataFrame({'col1': pd.Series([np.nan, np.nan])})
    sum_col = sum_column(df, 'col1')

    assert sum_col["result"] == 0


def test_sum_column_nonexistent_column():
    """ Test correct error if nonexistent column """

    df = pd.DataFrame({'col1': pd.Series([1, 4])})
    sum_col = sum_column(df, 'col9999')

    assert sum_col["error"] == "nonexistent column: col9999"


def test_sum_column_incorrect_type():
    """ Test correct error if wrong type of value in column """

    df = pd.DataFrame({'col1': pd.Series(["hello", 4])})
    sum_col = sum_column(df, 'col1')

    assert sum_col["error"] == "data with invalid type"


# # ####################################################
# # ############## Function rate_column() ##############
# # ####################################################


def test_rate_column_valid():
    """ Test correct result with valid data"""

    df = pd.DataFrame({'col1': pd.Series([1, 2]), 'col2': pd.Series([3, 4])})
    rate = rate_column(df, 'col1', 'col2')

    assert rate["result"] == 0.43


def test_rate_column_denominator_zero():
    """ Test null result if denominator is 0 """

    df = pd.DataFrame({'col1': pd.Series([1, 2]), 'col2': pd.Series([0, 0])})
    rate = rate_column(df, 'col1', 'col2')

    assert rate["result"] == 0


def test_rate_column_none_denominator():
    """ Test null result if denumerator column is full of NaN value """

    df = pd.DataFrame({'col1': pd.Series([1, 2]), 'col2': pd.Series([np.nan, np.nan])})
    rate = rate_column(df, 'col1', 'col2')

    assert rate["result"] == 0


def test_rate_column_none_numerator():
    """ Test result result if numerator column is full of NaN value """

    df = pd.DataFrame({'col1': pd.Series([np.nan, np.nan]), 'col2': pd.Series([1, 2])})
    rate = rate_column(df, 'col1', 'col2')

    assert rate["result"] == 0


def test_rate_column_incorrect_type():
    """ Test correct error if wrong type of value in column """

    df = pd.DataFrame({'col1': pd.Series(["hello", 4]), 'col2': pd.Series([1, 2])})
    rate = rate_column(df, 'col1', 'col2')

    assert rate["error"] == "data with invalid type"


def test_rate_column_nonexistent():
    """ Test correct error if nonexistent column """

    df = pd.DataFrame({'col1': pd.Series([1, 2]), 'col2': pd.Series([3, 4])})
    rate = rate_column(df, 'col1', 'col8888')

    assert rate["error"] == "nonexistent column: col8888"


# # #####################################################
# # ########### Function sum_groupby_column() ###########
# # #####################################################

def test_sum_groupby_one_column():
    """ Test correct result with one valid column data """

    countries = pd.Series(["Mexique", "Mexique", "Mexique", "Vietnam", "Vietnam", "Japon"])
    nb_hab = pd.Series([100, 250, 400, 50, 30, 700])

    df = pd.DataFrame({'countries': countries, 'nb_hab': nb_hab})
    sum_gb = sum_groupby_column(df, ["countries"], ["nb_hab"])
    result = sum_gb["result"].sort_values(by="countries").reset_index(drop=True)

    countries2 = pd.Series(["Mexique", "Vietnam", "Japon"])
    sum_c = pd.Series([750, 80, 700])
    expected = pd.DataFrame({"countries": countries2, "nb_hab": sum_c})
    expected = expected.sort_values(by="countries").reset_index(drop=True)

    assert_frame_equal(result, expected)


def test_sum_groupby_multiple_column_gp():
    """ Test correct result with two valid columns data """

    lang = pd.Series(["ESP", "ESP", "ESP", "ENG", "ENG", "ENG"])
    countries = pd.Series(["Mexique", "Mexique", "Mexique", "UK", "UK", "USA"])
    nb_hab = pd.Series([100, 250, 400, 50, 30, 700])

    df = pd.DataFrame({'lang': lang, 'countries': countries, 'nb_hab': nb_hab})
    sum_gb = sum_groupby_column(df, ["lang", "countries"], ["nb_hab"])
    result = sum_gb["result"].sort_values(by=["lang", "countries"]).reset_index(drop=True)

    lang = pd.Series(["ESP", "ENG", "ENG"])
    countries2 = pd.Series(["Mexique", "UK", "USA"])
    sum_c = pd.Series([750, 80, 700])
    expected = pd.DataFrame({"lang": lang, "countries": countries2, "nb_hab": sum_c})
    expected = expected.sort_values(by=["lang", "countries"]).reset_index(drop=True)

    assert_frame_equal(result, expected)


def test_sum_groupby_multiple_column_sum():
    """ Test correct result with two valid columns data """

    lang = pd.Series(["ESP", "ESP", "ESP", "ENG", "ENG", "ENG"])
    nb_hab = pd.Series([100, 250, 400, 50, 30, 700])
    idh = pd.Series([1, 2, 4, 5, 3, 7])

    df = pd.DataFrame({'lang': lang, 'nb_hab': nb_hab, 'idh': idh})
    sum_gb = sum_groupby_column(df, ["lang"], ["nb_hab", "idh"])
    result = sum_gb["result"].sort_values(by=["lang"]).reset_index(drop=True)

    lang = pd.Series(["ENG", "ESP"])
    nb_hab2 = pd.Series([780, 750])
    idh2 = pd.Series([15, 7])
    expected = pd.DataFrame({"lang": lang, "nb_hab": nb_hab2, "idh": idh2})
    expected = expected.sort_values(by=["lang"]).reset_index(drop=True)

    assert_frame_equal(result, expected)


def test_sum_groupby_nan_value():
    """ Test correct result even with nan value """

    countries = pd.Series(["UK", "UK", "USA"])
    nb_hab = pd.Series([100, np.nan, 400])

    df = pd.DataFrame({'countries': countries, 'nb_hab': nb_hab})
    sum_gb = sum_groupby_column(df, ["countries"], ["nb_hab"])
    result = sum_gb["result"].sort_values(by=["countries"]).reset_index(drop=True)

    countries2 = pd.Series(["UK", "USA"])
    # NaN is float64
    nb_hab2 = pd.Series([100.0, 400.0])
    expected = pd.DataFrame({"countries": countries2, "nb_hab": nb_hab2})
    expected = expected.sort_values(by=["countries"]).reset_index(drop=True)

    assert_frame_equal(result, expected)


def test_sum_groupby_empty_sum_column():
    """ Test null result if sum column is empty (groupby is then possible) """

    countries = pd.Series(["UK", "UK", "USA"])
    # In the future, empty Series will be considered as "object" type
    nb_hab = pd.Series([], dtype="float64")

    df = pd.DataFrame({'countries': countries, 'nb_hab': nb_hab})
    sum_gb = sum_groupby_column(df, ["countries"], ["nb_hab"])
    result = sum_gb["result"].sort_values(by=["countries"]).reset_index(drop=True)

    countries2 = pd.Series(["UK", "USA"])
    nb_hab2 = pd.Series([0.0, 0.0])
    expected = pd.DataFrame({"countries": countries2, "nb_hab": nb_hab2})
    expected = expected.sort_values(by=["countries"]).reset_index(drop=True)

    assert_frame_equal(result, expected)


def test_sum_groupby_nonexistent_gp_column():
    """ Test correct error if nonexistent column to group by"""

    countries = pd.Series(["UK", "UK", "USA"])
    nb_hab = pd.Series([100, 250, 400])

    df = pd.DataFrame({'countries': countries, 'nb_hab': nb_hab})
    sum_gb = sum_groupby_column(df, ["countries", "animals"], ["nb_hab"])

    assert sum_gb["error"] == "nonexistent column: animals"


def test_sum_groupby_nonexistent_sum_column():
    """ Test correct error if nonexistent column to sum """

    countries = pd.Series(["UK", "UK", "USA"])
    nb_hab = pd.Series([100, 250, 400])

    df = pd.DataFrame({'countries': countries, 'nb_hab': nb_hab})
    sum_gb = sum_groupby_column(df, ["countries"], ["toys"])

    assert sum_gb["error"] == "nonexistent column: toys"


def test_sum_groupby_incorrect_type():
    """ Test correct error if nonexistent column """

    countries = pd.Series(["UK", "UK", "USA"])
    nb_hab = pd.Series([100, "hello", 400])

    df = pd.DataFrame({'countries': countries, 'nb_hab': nb_hab})
    sum_gb = sum_groupby_column(df, ["countries"], ["nb_hab"])

    assert sum_gb["error"] == "data with invalid type"


def test_sum_groupby_empty_col_list():
    """ Test correct error if nonexistent column """

    countries = pd.Series(["UK", "UK", "USA"])
    nb_hab = pd.Series([100, "hello", 400])

    df = pd.DataFrame({'countries': countries, 'nb_hab': nb_hab})
    sum_gb = sum_groupby_column(df, [], ["nb_hab"])

    assert sum_gb["error"] == "no column to group by or to sum"


# # ############################################################
# # ############## Function rate_groupby_column() ##############
# # ############################################################

def test_rate_groupby_valid():
    """ Test correct result with valid data """

    lang = pd.Series(["ESP", "ESP", "ESP", "ENG", "ENG", "ENG"])
    countries = pd.Series(["Mexique", "Mexique", "Mexique", "UK", "UK", "USA"])
    pib = pd.Series([44, 55, 6, 23, 78, 11])
    nb_hab = pd.Series([100, 250, 400, 50, 300, 700])

    df = pd.DataFrame({
        'lang': lang, 'countries': countries,
        'nb_hab': nb_hab, 'pib': pib
    })
    rate = rate_groupby_column(df, ["lang", "countries"], "pib", "nb_hab")
    result = rate["result"].sort_values(by=["lang", "countries"]).reset_index(drop=True)

    lang = pd.Series(["ESP", "ENG", "ENG"])
    countries2 = pd.Series(["Mexique", "UK", "USA"])
    rate = pd.Series([0.14, 0.29, 0.02])
    expected = pd.DataFrame({"lang": lang, "countries": countries2, "rate": rate})
    expected = expected.sort_values(by=["lang", "countries"]).reset_index(drop=True)

    assert_frame_equal(result, expected)


def test_rate_groupby_denominator_zero():
    """ Test correct result if some denominator equal to zero  """

    lang = pd.Series(["ESP", "ESP", "ESP", "ENG", "ENG", "ENG"])
    countries = pd.Series(["Mexique", "Mexique", "Mexique", "UK", "UK", "USA"])
    pib = pd.Series([44, 55, 6, 23, 78, 11])
    nb_hab = pd.Series([100, 250, 400, 0, 0, 700])
    df = pd.DataFrame({
        'lang': lang, 'countries': countries,
        'nb_hab': nb_hab, 'pib': pib
    })

    rate = rate_groupby_column(df, ["lang", "countries"], "pib", "nb_hab")
    result = rate["result"].sort_values(by=["lang", "countries"]).reset_index(drop=True)

    lang = pd.Series(["ESP", "ENG", "ENG"])
    countries2 = pd.Series(["Mexique", "UK", "USA"])
    rate = pd.Series([0.14, 0.00, 0.02])
    expected = pd.DataFrame({"lang": lang, "countries": countries2, "rate": rate})
    expected = expected.sort_values(by=["lang", "countries"]).reset_index(drop=True)

    assert_frame_equal(result, expected)


def test_rate_groupby_none_denominator():
    """ Test correct result if some denominator equal to NaN  """

    lang = pd.Series(["ESP", "ESP", "ESP", "ENG", "ENG", "ENG"])
    countries = pd.Series(["Mexique", "Mexique", "Mexique", "UK", "UK", "USA"])
    pib = pd.Series([44, 55, 6, 23, 78, 11])
    nb_hab = pd.Series([100, 250, 400, np.nan, 300, np.nan])

    df = pd.DataFrame({
        'lang': lang, 'countries': countries,
        'nb_hab': nb_hab, 'pib': pib
    })
    rate = rate_groupby_column(df, ["lang", "countries"], "pib", "nb_hab")
    result = rate["result"].sort_values(by=["lang", "countries"]).reset_index(drop=True)

    lang = pd.Series(["ESP", "ENG", "ENG"])
    countries2 = pd.Series(["Mexique", "UK", "USA"])
    rate = pd.Series([0.14, 0.34, 0.00])
    expected = pd.DataFrame({"lang": lang, "countries": countries2, "rate": rate})
    expected = expected.sort_values(by=["lang", "countries"]).reset_index(drop=True)

    assert_frame_equal(result, expected)


# # ############################################################
# # ############## Function rate_groupby_column() ##############
# # ############################################################


def test_get_col_name_existing():

    countries = pd.Series(["Mexique", "Mexique", "Mexique", "Vietnam", "Vietnam", "Japon"])
    nb_hab = pd.Series([100, 250, 400, 50, 30, 700])
    df = pd.DataFrame({'countries': countries, 'nb_hab': nb_hab})

    name = get_col_name(df, "countries", "animals")
    assert name == "countries"


def test_get_col_name_default():

    countries = pd.Series(["Mexique", "Mexique", "Mexique", "Vietnam", "Vietnam", "Japon"])
    nb_hab = pd.Series([100, 250, 400, 50, 30, 700])
    df = pd.DataFrame({'countries': countries, 'nb_hab': nb_hab})

    name = get_col_name(df, "animals", "vegetables")
    assert name == "vegetables"


# # ############################################################
# # ############## Function get_top_n() ##############
# # ############################################################


def test_get_top_n_with_sort_col():

    countries = pd.Series(["Mexique", "Mexique", "Vietnam", "Japon"])
    nb_hab = pd.Series([100, 250, 400, 50])
    df = pd.DataFrame({'countries': countries, 'nb_hab': nb_hab})

    top = get_top_n(data=df, sort_col="nb_hab", ascending=True)
    top = top["result"].reset_index(drop=True)

    countries2 = pd.Series(["Japon", "Mexique", "Mexique", "Vietnam"])
    nb_hab2 = pd.Series([50, 100, 250, 400])
    expected = pd.DataFrame({"countries": countries2, "nb_hab": nb_hab2})

    assert_frame_equal(top, expected)


def test_get_top_n_limited_value():

    countries = pd.Series(["Mexique", "Mexique", "Vietnam", "Japon"])
    nb_hab = pd.Series([100, 250, 400, 50])
    df = pd.DataFrame({'countries': countries, 'nb_hab': nb_hab})

    top = get_top_n(data=df, sort_col="nb_hab", ascending=True, nb=2)
    top = top["result"].reset_index(drop=True)

    expected = pd.DataFrame({
        "countries": pd.Series(["Japon", "Mexique"]), "nb_hab": pd.Series([50, 100])
    })
    assert_frame_equal(top, expected)


def test_get_top_n_no_column():

    countries = pd.Series(["Mexique", "Mexique", "Vietnam", "Japon"])
    nb_hab = pd.Series([100, 250, 400, 50])
    df = pd.DataFrame({'countries': countries, 'nb_hab': nb_hab})

    top = get_top_n(data=df, sort_col=None, ascending=True)

    assert top["error"] == "no column to sort"


def test_get_top_n_nonexistent_column():

    countries = pd.Series(["Mexique", "Mexique", "Vietnam", "Japon"])
    nb_hab = pd.Series([100, 250, 400, 50])
    df = pd.DataFrame({'countries': countries, 'nb_hab': nb_hab})

    top = get_top_n(data=df, sort_col="animals", ascending=True)

    assert top["error"] == "nonexistent column: animals"


# # ############################################################
# # ############## Function add_all_to_timeline() ##############
# # ############################################################

def test_add_all_to_timeline_sum():

    lang = pd.Series(["ESP", "ESP", "ESP", "ENG", "ENG", "ENG"])
    countries = pd.Series(["Mexique", "Mexique", "Mexique", "UK", "UK", "USA"])
    nb_hab = pd.Series([100, 250, 400, 50, 300, 700])
    df = pd.DataFrame({'languages': lang, 'countries': countries, 'nb_hab': nb_hab})

    sum_gb = sum_groupby_column(df, ["languages", "countries"], ["nb_hab"])

    all_res = add_all_to_timeline(
        df, list_val=["ALL", "Mexique"], list_col_gb=["languages"],
        col1="nb_hab", col_name="countries", last_result=sum_gb["result"]
    )["result"]

    lang = pd.Series(["ENG", "ENG", "ESP", "ENG", "ESP"])
    countries = pd.Series(["UK", "USA", "Mexique", "ALL", "ALL"])
    nb_hab = pd.Series([350, 700, 750, 1050, 750])
    expected = pd.DataFrame({
        'languages': lang, 'countries': countries,
        'nb_hab': nb_hab
    })

    assert_frame_equal(all_res, expected)


def test_add_all_to_timeline_rate():
    lang = pd.Series(["ESP", "ESP", "ESP", "ENG", "ENG", "ENG"])
    countries = pd.Series(["Mexique", "Mexique", "Mexique", "UK", "UK", "USA"])
    pib = pd.Series([44, 55, 6, 23, 78, 11])
    nb_hab = pd.Series([100, 250, 400, 50, 300, 700])
    df = pd.DataFrame({
        'languages': lang, 'countries': countries,
        'pib': pib, 'nb_hab': nb_hab,
    })
    rate_gb = rate_groupby_column(df, ["languages", "countries"], "pib", "nb_hab")

    all_res = add_all_to_timeline(
        df, list_val=["ALL", "Mexique"], list_col_gb=["languages"],
        col1="pib", col2="nb_hab", col_name="countries", last_result=rate_gb["result"]
    )["result"]

    lang = pd.Series(["ENG", "ENG", "ESP", "ENG", "ESP"])
    countries = pd.Series(["UK", "USA", "Mexique", "ALL", "ALL"])
    rate_gb = pd.Series([0.29, 0.02, 0.14, 0.11, 0.14])
    expected = pd.DataFrame({
        'languages': lang, 'countries': countries,
        'rate': rate_gb
    })

    assert_frame_equal(all_res, expected)


def test_add_all_to_timeline_no_all():
    lang = pd.Series(["ESP", "ESP", "ESP", "ENG", "ENG", "ENG"])
    countries = pd.Series(["Mexique", "Mexique", "Mexique", "UK", "UK", "USA"])
    pib = pd.Series([44, 55, 6, 23, 78, 11])
    nb_hab = pd.Series([100, 250, 400, 50, 300, 700])
    df = pd.DataFrame({
        'languages': lang, 'countries': countries,
        'pib': pib, 'nb_hab': nb_hab
    })

    rate_gb = rate_groupby_column(df, ["languages", "countries"], "pib", "nb_hab")

    all_res = add_all_to_timeline(
        df,  list_val=["Mexique"], list_col_gb=["languages"],
        col1="pib", col2="nb_hab", col_name="countries", last_result=rate_gb["result"]
    )["result"]

    lang = pd.Series(["ENG", "ENG", "ESP"])
    countries = pd.Series(["UK", "USA", "Mexique"])
    rate_gb = pd.Series([0.29, 0.02, 0.14])
    expected = pd.DataFrame({
        'languages': lang, 'countries': countries,
        'rate': rate_gb
    })

    assert_frame_equal(all_res, expected)


def test_add_all_to_timeline_wrong_col_name_column():

    lang = pd.Series(["ESP", "ESP", "ESP", "ENG", "ENG", "ENG"])
    countries = pd.Series(["Mexique", "Mexique", "Mexique", "UK", "UK", "USA"])
    nb_hab = pd.Series([100, 250, 400, 50, 300, 700])
    df = pd.DataFrame({'languages': lang, 'countries': countries, 'nb_hab': nb_hab})

    sum_gb = sum_groupby_column(df, ["languages", "countries"], ["nb_hab"])

    all_res = add_all_to_timeline(
        df, list_val=["ALL", "Mexique"], list_col_gb=["languages"],
        col1="nb_hab", col_name="animals", last_result=sum_gb["result"]
    )

    assert all_res["error"] == "nonexistent column: animals"


def test_add_all_to_timeline_wrong_list_col_gb():

    lang = pd.Series(["ESP", "ESP", "ESP", "ENG", "ENG", "ENG"])
    countries = pd.Series(["Mexique", "Mexique", "Mexique", "UK", "UK", "USA"])
    nb_hab = pd.Series([100, 250, 400, 50, 300, 700])
    df = pd.DataFrame({'languages': lang, 'countries': countries, 'nb_hab': nb_hab})

    sum_gb = sum_groupby_column(df, ["languages", "countries"], ["nb_hab"])

    all_res = add_all_to_timeline(
        df, list_val=["ALL", "Mexique"], list_col_gb=["Mexique"],
        col1="nb_hab", col_name="nb_hab", last_result=sum_gb["result"]
    )

    assert all_res["error"] == "nonexistent column: Mexique"


def test_add_all_to_timeline_col_not_in_last_result():

    lang = pd.Series(["ESP", "ESP", "ESP", "ENG", "ENG", "ENG"])
    countries = pd.Series(["Mexique", "Mexique", "Mexique", "UK", "UK", "USA"])
    nb_hab = pd.Series([100, 250, 400, 50, 300, 700])
    df = pd.DataFrame({'languages': lang, 'countries': countries, 'nb_hab': nb_hab})

    sum_gb = sum_groupby_column(df, ["languages"], ["nb_hab"])

    all_res = add_all_to_timeline(
        df, list_val=["ALL", "Mexique"], list_col_gb=["languages"],
        col1="nb_hab", col_name="countries", last_result=sum_gb["result"]
    )

    assert all_res["error"] == "nonexistent column: countries"


def test_add_all_to_timeline_none_last_result():

    lang = pd.Series(["ESP", "ESP", "ESP", "ENG", "ENG", "ENG"])
    countries = pd.Series(["Mexique", "Mexique", "Mexique", "UK", "UK", "USA"])
    nb_hab = pd.Series([100, 250, 400, 50, 300, 700])
    df = pd.DataFrame({'languages': lang, 'countries': countries, 'nb_hab': nb_hab})

    all_res = add_all_to_timeline(
        df, list_val=["ALL", "Mexique"], list_col_gb=["languages"],
        col1="nb_hab", col_name="countries", last_result=None
    )

    assert all_res["error"] == "last_result is None"


# # ####################################################
# # ############## Function filter_line_cube() ##############
# # ####################################################


def test_filter_line_cube_valid_parameter():

    lang = pd.Series(["ESP", "ESP", "ESP", "ENG", "ENG", "ENG"])
    countries = pd.Series(["Mexique", "Mexique", "Mexique", "UK", "UK", "USA"])
    df = pd.DataFrame({'languages': lang, 'countries': countries})

    filter_c = filter_line_cube(df, "countries", ["UK"])["result"].reset_index(drop=True)

    expected = pd.DataFrame(
        {"languages": ["ENG", "ENG"], "countries": ["UK", "UK"]}
    ).reset_index(drop=True)

    assert_frame_equal(filter_c, expected)


def test_filter_line_cube_empty_list_values():

    lang = pd.Series(["ESP", "ESP", "ESP", "ENG", "ENG", "ENG"])
    countries = pd.Series(["Mexique", "Mexique", "Mexique", "UK", "UK", "USA"])
    df = pd.DataFrame({'languages': lang, 'countries': countries})

    filter_c = filter_line_cube(df, "countries", [])["result"]

    assert_frame_equal(filter_c, df)


def test_filter_line_cube_all_values():

    lang = pd.Series(["ESP", "ESP", "ESP", "ENG", "ENG", "ENG"])
    countries = pd.Series(["Mexique", "Mexique", "Mexique", "UK", "UK", "USA"])
    df = pd.DataFrame({'languages': lang, 'countries': countries})

    filter_c = filter_line_cube(df, "countries", ["ALL"])["result"]

    assert_frame_equal(filter_c, df)


def test_filter_line_cube_nonexistent_column():

    lang = pd.Series(["ESP", "ESP", "ESP", "ENG", "ENG", "ENG"])
    countries = pd.Series(["Mexique", "Mexique", "Mexique", "UK", "UK", "USA"])
    df = pd.DataFrame({'languages': lang, 'countries': countries})

    filter_c = filter_line_cube(df, "animals", ["UK"])

    assert filter_c["error"] == "nonexistent column: animals"


# # ####################################################
# # ########## Function remove_small_inent() ###########
# # ####################################################


def test_remove_small_intent_valid():

    conv = pd.Series(["perdu code puk", "consulter facture", "besoin info", "besoin technicien"])
    intent = pd.Series(["perte-code", "small-consult", "small-info", "aide-technicien"])
    df = pd.DataFrame({"conversation": conv, "intent": intent})

    remove = remove_small_intent(df)["result"].reset_index(drop=True)

    expected = pd.DataFrame(
        {"conversation": ["perdu code puk", "besoin technicien"],
         "intent": ["perte-code", "aide-technicien"]}
    )

    assert_frame_equal(remove, expected)


def test_remove_small_intent_no_intent_column():
    conv = pd.Series(["perdu code puk", "consulter facture", "besoin info", "besoin technicien"])
    df = pd.DataFrame({"conversation": conv})

    remove = remove_small_intent(df)

    assert remove["error"] == "column 'intent' not existing in data"
