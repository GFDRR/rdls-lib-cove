import json
from typing import Optional
from urllib.parse import urlparse

import jsonref  # type: ignore
from libcove2.common import schema_dict_fields_generator  # type: ignore
from packaging import version as packaging_version

import libcoverdls.data_reader
from libcoverdls.config import LibCoveRDLSConfig

try:
    from functools import cached_property
except ImportError:
    from cached_property import cached_property  # type: ignore


class SchemaRDLS:
    def __init__(
        self,
        data_reader: Optional[libcoverdls.data_reader.DataReader] = None,
        lib_cove_rdls_config=None,
    ):
        self.config = lib_cove_rdls_config or LibCoveRDLSConfig()
        # Information about this schema
        # ... what version the data tried to set (used later to check for inconsistent statements)
        self.schema_version_attempted = None
        # ... what version we actually use
        self.schema_version = None
        # ... resources for the version we are actually using
        self.pkg_schema_url = None
        self.schema_url = None
        self.schema_host = None
        # ... any error encountered when working out the version
        self.schema_error: Optional[dict] = None
        # Now try to work out version from information passed
        self.__work_out_schema_version(data_reader)

    def __work_out_schema_version(
        self, data_reader: Optional[libcoverdls.data_reader.DataReader] = None
    ):

        # If no data is passed, then we assume it's the default version
        if not data_reader:
            self.schema_url = self.config.config["schema_pkg_url"]
            self.pkg_schema_url = self.config.config["schema_url"]
            self.schema_host = self.config.config["schema_url_host"]
            self.schema_version_attempted = self.config.config["schema_version"]
            self.schema_version = self.config.config["schema_version"]
            return

        # If bad data passed, then we assume it's the default version
        all_data = data_reader.get_all_data()
        if not isinstance(all_data, list) or len(all_data) == 0:
            self.schema_url = self.config.config["schema_pkg_url"]
            self.pkg_schema_url = self.config.config["schema_url"]
            self.schema_host = self.config.config["schema_url_host"]
            self.schema_version_attempted = self.config.config["schema_version"]
            self.schema_version = self.config.config["schema_version"]
            return

        self.schema_url = self.config.config["schema_pkg_url"]
        self.pkg_schema_url = self.config.config["schema_url"]
        self.schema_host = self.config.config["schema_url_host"]
        self.schema_version_attempted = self.config.config["schema_version"]
        self.schema_version = self.config.config["schema_version"]
        return

    def is_schema_version_equal_to_or_greater_than(self, version):
        return packaging_version.parse(self.schema_version) >= packaging_version.parse(
            version
        )

    def get_package_schema_fields(self) -> set:
        return set(schema_dict_fields_generator(self._pkg_schema_obj_ref))

    @cached_property
    def pkg_schema_str(self):
        uri_scheme = urlparse(self.pkg_schema_url).scheme
        if uri_scheme == "http" or uri_scheme == "https":
            raise NotImplementedError(
                "Downloading schema files over HTTP/HTTPS is not supported"
            )
        else:
            with open(self.pkg_schema_url) as fp:
                return fp.read()

    @property
    def _pkg_schema_obj_ref(self):
        return jsonref.loads(self.pkg_schema_str)

    @property
    def _pkg_schema_obj(self):
        return json.loads(self.pkg_schema_str)
