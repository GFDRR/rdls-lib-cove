import os
import tempfile

from tests.api import rdls_json_output


def test_additional_field():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-rdls-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.2",
        "complete-additional.json",
    )

    results = rdls_json_output(cove_temp_folder, json_filename)

    for result in results:
        print(result, results[result])

    assert results["schema_version"] == "0.2"
    assert results["file_type"] == "json"

    assert results["additional_fields_count"] == 1
    assert "/test_additional" in results["additional_fields"]
