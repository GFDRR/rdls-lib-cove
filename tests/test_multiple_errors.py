import os
import tempfile
from collections import defaultdict

from tests.api import rdls_json_output


def test_multiple_errors():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-rdls-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.2",
        "multiple-errors.json",
    )

    results = rdls_json_output(cove_temp_folder, json_filename)

    for result in results:
        print(result, results[result])

    assert results["schema_version"] == "0.2"
    assert results["file_type"] == "json"

    assert results["validation_errors_count"] == 4

    counts = defaultdict(lambda: 0)
    for error in results["validation_errors"]:
        if (
            error["path_ending"] == "risk_data_type"
            and error["validator"] == "type"
            and error["validator_value"] == "array"
        ):
            counts["risk_data_type"] += 1
        if (
            error["path_ending"] == "id"
            and error["validator"] == "type"
            and error["validator_value"] == "string"
            and error["instance"] == 1
        ):
            counts["id_1"] += 1
        if (
            error["path_ending"] == "id"
            and error["validator"] == "type"
            and error["validator_value"] == "string"
            and error["instance"] == 2
        ):
            counts["id_2"] += 1
        if (
            error["path_ending"] == "href"
            and error["validator"] == "const"
            and error["validator_value"]
            == "https://docs.riskdatalibrary.org/en/0__2__0/rdls_schema.json"
        ):
            counts["href"] += 1

    assert counts["risk_data_type"] == 1
    assert counts["id_1"] == 1
    assert counts["id_2"] == 1
    assert counts["href"] == 1

    assert results["additional_fields_count"] == 1
    assert "/resources/url" in results["additional_fields"]
