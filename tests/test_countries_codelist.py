import os
import tempfile

from tests.api import rdls_json_output


def test_multiple_errors():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-rdls-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.2",
        "countries_codelist.json",
    )

    results = rdls_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.2"
    assert results["file_type"] == "json"

    assert results["validation_errors_count"] == 2

    for error in results["validation_errors"]:
        assert error["validator"] == "enum"
        assert error["path_ending"] == "countries/[number]"
        assert error["instance"] in ("A", "B")
