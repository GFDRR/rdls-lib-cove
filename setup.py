from setuptools import find_packages, setup

setup(
    name="libcoverdls",
    version="0.1.0",
    author="Open Data Services",
    author_email="code@opendataservices.coop",
    url="https://github.com/openownership/rdls-lib-cove",
    description="A data review library",
    packages=find_packages(),
    long_description="A data review library",
    python_requires=">=3.8",
    install_requires=[
        "python-dateutil",
        "libcove2",
        "packaging",
        "jsonschema",
        "pytz",
        "ijson",
        # Required for jsonschema to validate URIs
        "rfc3987",
        # Required for jsonschema to validate date-time
        "rfc3339-validator",
    ],
    extras_require={"dev": ["pytest", "flake8", "black==22.3.0", "isort", "mypy"]},
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    ],
    entry_points="""[console_scripts]
libcoverdls = libcoverdls.cli:main""",
    include_package_data=True,
)
