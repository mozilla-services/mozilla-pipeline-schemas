from setuptools import setup, find_namespace_packages

setup(
    name="mozilla-pipeline-schemas",
    version="0.2.0",
    use_incremental=True,
    author="Mozilla Corporation",
    author_email="fx-data-dev@mozilla.org",
    description="Tooling for managing schemas for schema ingestion",
    url="https://github.com/mozilla-services/mozilla-pipeline-schemas",
    packages=find_namespace_packages(
        include=["mozilla_pipeline_schemas.*", "mozilla_pipeline_schemas"]
    ),
    package_data={},
    include_package_data=True,
    install_requires=["click"],
    long_description="Tooling for managing schemas for schema ingestion",
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    entry_points="""
        [console_scripts]
        mps=mozilla_pipeline_schemas.cli:entry_point
    """,
)
