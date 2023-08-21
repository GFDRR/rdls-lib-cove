import json
import os
import tempfile

import pytest

from libcoverdls.config import LibCoveRDLSConfig
from tests.api import rdls_json_output


def test_basic_1():

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-rdls-tests-", dir=tempfile.gettempdir()
    )
    json_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "fixtures", "0.1", "complete.json"
    )

    results = rdls_json_output(cove_temp_folder, json_filename)

    assert results["schema_version"] == "0.1"
    assert results["validation_errors_count"] == 0
    assert results["additional_fields_count"] == 150
    assert results["additional_checks_count"] == 0
    assert results["file_type"] == "json"
#    assert results["statistics"]["count_entity_statements"] == 1
#    for k in results["statistics"]["count_entity_statements_types"]:
#        if k == "registeredEntity":
#            assert results["statistics"]["count_entity_statements_types"][k] == 1
#        else:
#            assert results["statistics"]["count_entity_statements_types"][k] == 0
#    for k in results["statistics"]["count_entity_statements_types_with_any_identifier"]:
#        if k == "registeredEntity":
#            assert (
#                results["statistics"][
#                    "count_entity_statements_types_with_any_identifier"
#                ][k]
#                == 1
#            )
#        else:
#            assert (
#                results["statistics"][
#                    "count_entity_statements_types_with_any_identifier"
#                ][k]
#                == 0
#            )
#    for k in results["statistics"][
#        "count_entity_statements_types_with_any_identifier_with_id_and_scheme"
#    ]:
#        if k == "registeredEntity":
#            assert (
#                results["statistics"][
#                    "count_entity_statements_types_with_any_identifier_with_id_and_scheme"
#                ][k]
#                == 1
#            )  # noqa
#        else:
#            assert (
#                results["statistics"][
#                    "count_entity_statements_types_with_any_identifier_with_id_and_scheme"
#                ][k]
#                == 0
#            )  # noqa
#
#    assert results["statistics"]["count_person_statements"] == 1
#    for k in results["statistics"]["count_person_statements_types"]:
#        if k == "knownPerson":
#            assert results["statistics"]["count_person_statements_types"][k] == 1
#        else:
#            assert results["statistics"]["count_person_statements_types"][k] == 0
#    assert results["statistics"]["count_ownership_or_control_statement"] == 1
#    assert results["statistics"]["count_ownership_or_control_statement_current"] == 1
#    assert (
#        results["statistics"][
#            "count_ownership_or_control_statement_interested_party_with_person"
#        ]
#        == 1
#    )
#    assert (
#        results["statistics"][
#            "count_ownership_or_control_statement_interested_party_with_entity"
#        ]
#        == 0
#    )
#    assert (
#        results["statistics"][
#            "count_ownership_or_control_statement_interested_party_with_unspecified"
#        ]
#        == 0
#    )
#    for k in results["statistics"][
#        "count_ownership_or_control_statement_interest_statement_types"
#    ]:
#        if k == "shareholding":
#            assert (
#                results["statistics"][
#                    "count_ownership_or_control_statement_interest_statement_types"
#                ][k]
#                == 1
#            )
#        else:
#            assert (
#                results["statistics"][
#                    "count_ownership_or_control_statement_interest_statement_types"
#                ][k]
#                == 0
#            )
#    assert results["statistics"]["count_replaces_statements_missing"] == 0

