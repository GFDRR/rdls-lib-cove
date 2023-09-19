import json
import os

import libcoverdls.data_reader


def test_full_get_all_data_1():

    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "fixtures", "0.2", "basic_1.json"
    )

    with open(json_filename) as fp:
        expected = json.load(fp)["datasets"]

    data_reader = libcoverdls.data_reader.DataReader(json_filename)
    actual = data_reader.get_all_data()

    assert expected == actual


def test_sample_but_no_change_get_all_data_1():

    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.2",
        "basic_extra_1.json",
    )

    with open(json_filename) as fp:
        expected = json.load(fp)["datasets"]

    data_reader = libcoverdls.data_reader.DataReader(
        json_filename, sample_mode=True, sample_mode_max_row_count=5
    )
    actual = data_reader.get_all_data()

    # In this case the input file has way less than 50 of each type, so we expect exactly the same
    assert len(expected) == len(actual)


def test_sample_some_removed_get_all_data_1():

    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.2",
        "basic_extra_1.json",
    )

    with open(json_filename) as fp:
        input = json.load(fp)["datasets"]
    expected = [
        input[0],
        input[1],
        input[2],
    ]

    data_reader = libcoverdls.data_reader.DataReader(
        json_filename, sample_mode=True, sample_mode_max_row_count=3
    )
    actual = data_reader.get_all_data()

    # In this case the input file has way less than 50 of each type, so we expect exactly the same
    assert len(expected) == len(actual)


def test_sample_bad_statements_are_included_get_all_data_1():

    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.2",
        "badfile_all_validation_errors.json",
    )

    with open(json_filename) as fp:
        input = json.load(fp)["datasets"]
    expected = [
        input[0],
        input[1],
        #        input[2],
        #        input[4],
        #        input[16],
        #        input[17],
        #        input[21],
    ]

    data_reader = libcoverdls.data_reader.DataReader(
        json_filename, sample_mode=True, sample_mode_max_row_count=2
    )
    actual = data_reader.get_all_data()

    # In this case the input file has way less than 50 of each type, so we expect exactly the same
    assert expected == actual
