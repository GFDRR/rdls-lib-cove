import os
import json
from decimal import Decimal
from collections import namedtuple

from jsonschema import FormatChecker
from jsonschema.exceptions import ValidationError
from jsonschema.validators import Draft4Validator, Draft202012Validator

import libcoverdls.data_reader
from libcoverdls.schema import SchemaRDLS


class NumberStr(float):
    def __init__(self, o):
        # We don't call the parent here, since we're deliberately altering it's functionality
        # pylint: disable=W0231
        self.o = o

    def __repr__(self):
        return str(self.o)

    # This is needed for this trick to work in python 3.4
    def __float__(self):
        return self


def decimal_default(o):
    if isinstance(o, Decimal):
        if int(o) == o:
            return int(o)
        else:
            return NumberStr(o)
    raise TypeError(f"{repr(o)} is not JSON serializable")


def oneOf_draft4(validator, oneOf, instance, schema):
    """
    oneOf_draft4 validator from
    https://github.com/Julian/jsonschema/blob/d16713a4296663f3d62c50b9f9a2893cb380b7af/jsonschema/_validators.py#L337
    Modified to:
    - sort the instance JSON, so we get a reproducible output that we
      can can test more easily
    - If `statementType` is available, use that pick the correct
      sub-schema, and to yield those ValidationErrors. (Only
      applicable for BODS).
    """
    subschemas = enumerate(oneOf)
    all_errors = []
    validStatementTypes = []
    for index, subschema in subschemas:
        errs = list(validator.descend(instance, subschema, schema_path=index))
        if not errs:
            first_valid = subschema
            break
        properties = subschema.get("properties", {})
        if "statementType" in properties:
            if "statementType" in instance:
                try:
                    validStatementType = properties["statementType"].get("enum", [])[0]
                except IndexError:
                    continue
                if instance["statementType"] == validStatementType:
                    for err in errs:
                        yield err
                    return
                else:
                    validStatementTypes.append(validStatementType)
            else:
                yield ValidationError(
                    "statementType",
                    validator="required",
                )
                break
        all_errors.extend(errs)
    else:
        if validStatementTypes:
            yield ValidationError(
                "Invalid code found in statementType",
                instance=instance["statementType"],
                path=("statementType",),
                validator="enum",
            )
        else:
            yield ValidationError(
                "%s is not valid under any of the given schemas"
                % (json.dumps(instance, sort_keys=True, default=decimal_default),),
                context=all_errors,
            )

    more_valid = [s for i, s in subschemas if validator.evolve(schema=s).is_valid(instance)]
    if more_valid:
        more_valid.append(first_valid)
        reprs = ", ".join(repr(schema) for schema in more_valid)
        yield ValidationError("%r is valid under each of %s" % (instance, reprs))


class JSONSchemaValidator:
    """Validates data using the JSON Schema method"""

    def __init__(self, schema: SchemaRDLS):
        self._schema = schema

    def _source_maps(self, data_reader):
        directory = data_reader._filename.rsplit("/", 1)[0]
        filename = data_reader._filename.split("/")[-1]
        if filename == "unflattened.json":
            cell_map_path = os.path.join(directory, "cell_source_map.json")
            heading_map_path = os.path.join(directory, "heading_source_map.json")
            if os.path.isfile(cell_map_path) and os.path.isfile(heading_map_path):
                with open(cell_map_path) as cell_source_map_fp:
                    cell_source_map = json.load(cell_source_map_fp)
                with open(heading_map_path) as heading_source_map_fp:
                    heading_source_map = json.load(heading_source_map_fp)
                return cell_source_map, heading_source_map
        return None, None

    def validate(self, data_reader: libcoverdls.data_reader.DataReader) -> list:
        """Call with data. Results are returned."""
        validator = Draft202012Validator(
            schema=self._schema._pkg_schema_obj, format_checker=FormatChecker()
        )
        #validator.VALIDATORS["oneOf"] = oneOf_draft4
        output = []
        cell_source_map, heading_source_map = self._source_maps(data_reader)
        all_data = data_reader.get_all_data()
        if all_data:
            for dataset_number, dataset in enumerate(all_data):
                #print("Dataset:", type(dataset))
                for e in validator.iter_errors(dataset):
                    output.append(RDLSValidationError(e, dataset, self._schema,
                                                 cell_source_map=cell_source_map,
                                                 heading_source_map=heading_source_map, 
                                                 dataset_number=dataset_number))
        else:
            DummyError = namedtuple("DummyError", ["message",
                                                   "path",
                                                   "schema_path",
                                                   "validator",
                                                   "validator_value",
                                                   "context",
                                                   "instance"])
            e = DummyError(message="'datsets' is a required property",
                           path=[],
                           schema_path=['datasets'],
                           validator="required",
                           validator_value="datasets",
                           context=None,
                           instance=all_data)
            output.append(RDLSValidationError(e, all_data, self._schema,
                                                 cell_source_map=cell_source_map,
                                                 heading_source_map=heading_source_map, 
                                                 dataset_number=0))
        return output


class RDLSValidationError:
    """Any problems found in data are returned as an instance of this class."""

    def __init__(
        self,
        json_schema_exceptions_validation_error: ValidationError,
        json_data: dict,
        schema: SchemaRDLS,
        cell_source_map: dict = None,
        heading_source_map: dict = None,
        dataset_number=0
    ):
        self._message = json_schema_exceptions_validation_error.message
        self._path = json_schema_exceptions_validation_error.path
        self._schema_path = json_schema_exceptions_validation_error.schema_path
        self._validator = json_schema_exceptions_validation_error.validator
        self._validator_value = json_schema_exceptions_validation_error.validator_value
        self._context = json_schema_exceptions_validation_error.context
        self._instance = json_schema_exceptions_validation_error.instance
        self._extra = {}

        self.cell_src_map = cell_source_map
        self.heading_src_map = heading_source_map
        self._dataset_number = dataset_number

        if self._validator == "required":
            if "'" in self._message:
                self._extra["required_key_which_is_missing"] = self._message.split("'")[
                    1
                ]
            else:
                self._extra["required_key_which_is_missing"] = self._message

    def _spreadsheet_location(self):
        path = "/".join(str(item) for item in self._path)
        path = f"datasets/{self._dataset_number}/{path}"
        path_no_number = "/".join(
            str(item) for item in self._path if not isinstance(item, int)
        )
        value = {"path": path}
        cell_reference = self.cell_src_map.get(path)

        if cell_reference:
            first_reference = cell_reference[0]
            if len(first_reference) == 4:
                (
                    value["sheet"],
                    value["col_alpha"],
                    value["row_number"],
                    value["header"],
                ) = first_reference
            if len(first_reference) == 2:
                value["sheet"], value["row_number"] = first_reference

        heading = self.heading_src_map.get(f"{path_no_number}/{self._message}")
        if heading:
            field_name = heading[0][1]
            value["header"] = heading[0][1]
        return value

    def json(self):
        """Return representation of this error in JSON."""

        #for name in self.__dir__():
        #    print(name, getattr(self, name))
        if len(self._path) > 0:
            path_ending = self._path[-1]
            if isinstance(self._path[-1], int) and len(self._path) >= 2:
                # We're dealing with elements in an array of items at this point
                path_ending = "{}/[number]".format(self._path[-2])
            elif isinstance(self._path[0], int) and len(self._path) == 1:
                path_ending = "[number]"
        else:
            if self._validator == "required":
                path_ending = self._extra['required_key_which_is_missing']
            else:
                path_ending = ""
        data = {
            "message": self._message,
            "path": list(self._path),
            "path_ending": path_ending,
            "schema_path": list(self._schema_path),
            "validator": self._validator,
            "validator_value": self._validator_value,
            # "context": self._context,
            "instance": self._instance,
            "extra": self._extra,
        }
        if self.cell_src_map:
            location = self._spreadsheet_location()
            data['location'] = location
        return data

