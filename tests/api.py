import libcoverdls.additionalfields
import libcoverdls.config
import libcoverdls.data_reader
import libcoverdls.jsonschemavalidate
import libcoverdls.run_tasks
import libcoverdls.schema


def rdls_json_output(
    temp_folder,
    input_file_name,
    file_type=None,
    json_data=None,
    lib_cove_rdls_config=None,
):
    # Data Reader
    data_reader = libcoverdls.data_reader.DataReader(input_file_name)

    # classes
    if not lib_cove_rdls_config:
        lib_cove_rdls_config = libcoverdls.config.LibCoveRDLSConfig()
    schema = libcoverdls.schema.SchemaRDLS(data_reader, lib_cove_rdls_config)

    # Additional checks and stats
    output_data = libcoverdls.run_tasks.process_additional_checks(
        data_reader, lib_cove_rdls_config, schema
    )

    # Additional fields
    additionalfields_validator = libcoverdls.additionalfields.AdditionalFields(schema)
    additionalfields_output = additionalfields_validator.process(data_reader)

    # JSON Schema
    jsonschemavalidate_validator = libcoverdls.jsonschemavalidate.JSONSchemaValidator(
        schema
    )
    jsonschemavalidate_output = jsonschemavalidate_validator.validate(data_reader)

    # Put it all together ...
    return {
        "schema_version": schema.schema_version,
        "additional_checks": output_data["additional_checks"],
        "additional_checks_count": len(output_data["additional_checks"]),
        "statistics": output_data["statistics"],
        "validation_errors_count": len(jsonschemavalidate_output),
        "validation_errors": [o.json() for o in jsonschemavalidate_output],
        "additional_fields_count": len(additionalfields_output),
        "additional_fields": additionalfields_output,
        "file_type": "json",
    }
