import datetime
from collections import namedtuple

from dateutil import parser
from pytz import UTC


def get_version_from_schema_url(dataset):
    if 'links' in dataset and len(dataset['links']) > 0:
        if 'href' in dataset['links'][0] and 'rel' in dataset['links'][0]: 
            if dataset['links'][0]['rel'] == 'describedby':
                schema_url = dataset['links'][0]['href']
                parts = schema_url.split("__")
                parts[0] = parts[0].split("/")[-1]
                parts[-1] = parts[-1].split("/")[0]
                version = ".".join(parts)
                return version
    return None


def create_dummy_error(message, schema_path, validator, validator_value, data):
    DummyError = namedtuple("DummyError", ["message",
                                           "path",
                                           "schema_path",
                                           "validator",
                                           "validator_value",
                                           "context",
                                           "instance"])
    error = DummyError(message=message,
                       path=[],
                       schema_path=schema_path,
                       validator=validator,
                       validator_value=validator_value,
                       context=None,
                       instance=data)
    return error

def get_year_from_bods_birthdate_or_deathdate(data):
    if len(data) == 4:
        return int(data)
    if len(data) > 4 and data[4] == "-":
        return int(data[0:4])


def is_interest_current(interest):
    if "endDate" in interest:
        try:
            nowUTC = datetime.datetime.now(UTC)
            endDate = parser.parse(interest["endDate"], default=nowUTC)
            if not endDate.tzinfo:
                endDate = endDate.replace(tzinfo=UTC)
            return endDate >= nowUTC
        except ValueError:
            return False
    else:
        return True
