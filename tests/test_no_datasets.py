import json
import os
import tempfile

import pytest

from libcoverdls.config import LibCoveRDLSConfig
from tests.api import rdls_json_output


def test_no_datasets():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-rdls-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "fixtures", "0.1", "no_datasets.json"
    )

    results = rdls_json_output(cove_temp_folder, json_filename)

    for result in results:
        print(result, results[result])

    assert results["schema_version"] == "0.2"
    assert results["file_type"] == "json"

    assert False

