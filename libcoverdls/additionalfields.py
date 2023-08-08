from libcove2.common import get_additional_fields_info  # type: ignore

import libcoverdls.data_reader
from libcoverdls.schema import SchemaRDLS


class AdditionalFields:
    """Process data and return additional fields information"""

    def __init__(self, schema: SchemaRDLS):
        self._schema = schema

    def process(self, data_reader: libcoverdls.data_reader.DataReader) -> list:
        """Process method. Call with data. Results are returned."""

        schema_fields = self._schema.get_package_schema_fields()

        additional_fields = get_additional_fields_info(
            data_reader.get_all_data(), schema_fields
        )

        return additional_fields
