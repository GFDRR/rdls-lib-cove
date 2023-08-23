import json
import os
import tempfile

import pytest

from libcoverdls.config import LibCoveRDLSConfig
from tests.api import rdls_json_output


def test_specific_links_rel():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-rdls-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "fixtures", "0.1", "links-broken.json"
    )

    results = rdls_json_output(cove_temp_folder, json_filename)

    d_count = 0
    s_count = 0
    for error in results['validation_errors']:
        print(error['message'])
        if "describedby" in error['message']: d_count += 1
        if 'https://raw.githubusercontent.com/GFDRR/rdl-standard/0__2__0/schema/rdls_schema.json' in error['message']: s_count += 1
    assert d_count == 2
    assert s_count == 1

    assert results["schema_version"] == "0.1"
    assert results["file_type"] == "json"
