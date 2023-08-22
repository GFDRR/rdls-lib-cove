import os
import tempfile

from tests.api import rdls_json_output


def test_schema_0_1_file_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-rdls-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "0.1",
        "rdls_hzd-FTH-THA.json",
    )

    results = rdls_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.1"

    assert results["validation_errors_count"] == 0
    assert results["additional_checks_count"] == 1
