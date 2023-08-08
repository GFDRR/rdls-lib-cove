# Lib Cove RDLS

This repository supports the RDLS Conversion and Validation Tool [(rdls-cove)](https://github.com/GFDRR/rdls-cove), which can be used by data publishers to create metadata for the [Risk data Library Standard](https://github.com/GFDRR/rdl-standard), by converting the [spreadsheet template](https://github.com/GFDRR/rdls-spreadsheet-template) to the JSON metadata format.

Documented at [rdl-standard.readthedocs.io](https://rdl-standard.readthedocs.io/en/latest/).
Documentation is maintained at [github.com/GFDRR/rdl-standard](https://github.com/GFDRR/rdl-standard).

## Command line

### Installation

Installation from this git repo:

```bash
git clone https://github.com/openownership/lib-cove-rdls.git
cd lib-cove-rdls
python3 -m venv .ve
source .ve/bin/activate
pip install -e .
```

### Running the command line tool

Call `libcoverdls`.

    libcoverdls -h
    
### Running tests

    python -m pytest

### Code linting

Make sure dev dependencies are installed in your virtual environment:

    pip install -e .[dev]

Then run:

    isort libcoverdls/ tests/ setup.py
    black libcoverdls/ tests/ setup.py
    flake8 libcoverdls/ tests/ setup.py

### Updating schema files in data

This library contains the actual data files for different versions of the schema, in the `libcoverdls/data` directory.

To update them, you need:
 * a install of the Compile To JSON Schema Tool. https://compiletojsonschema.readthedocs.io/en/latest/index.html
 * a checkout of the data standard repository. https://github.com/GFDRR/rdl-standard

To update a file:

First go to your checkout of the data standard repository and make sure you have checked out the correct tag or branch.
ie. To update the `libcoverdls/data/schema-0-1-0.json` file, check out `0.1.0`

Run the compile tool, telling it where the codelists directory is and pipe the output to the file for the version 
you have checked out:

    compiletojsonschema -c rdl-standard/codelists/closed/ rdl-standard/schema/rdl_schema_0.1.json > rdls-lib-cove/libcoverdls/data/schema-0-1-0.json
