import os

_schema_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

LIB_COVE_RDLS_CONFIG_DEFAULT = {
    # These details are used if the data does not specify a version
    "schema_url": os.path.join(_schema_folder, "schema-0-2-0.json"),
    "schema_pkg_url": os.path.join(_schema_folder, "rdls_package_schema.json"),
    "schema_url_host": _schema_folder,
    "schema_version": "0.2",
    # But from 0.2 onwards, data should specify a version
    "schema_versions": {
        "0.2": {
            "schema_url": os.path.join(_schema_folder, "schema-0-2-0.json"),
            "schema_url_host": _schema_folder,
        },
    },
    # In some cases we default to the latest schema version, so we need to know what the latest version is.
    # It should be a key that is in the 'schema_versions' data.
    "schema_latest_version": "0.2",
    # These default values are very wide on purpose. It is left to apps using this to tighten them up.
}


class LibCoveRDLSConfig:
    def __init__(self, config=None):
        # We need to make sure we take a copy,
        #   so that changes to one config object don't end up effecting other config objects.
        if config:
            self.config = config.copy()
        else:
            self.config = LIB_COVE_RDLS_CONFIG_DEFAULT.copy()
