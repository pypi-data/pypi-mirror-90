# from pathlib import Path
import setuptools

setuptools.setup(
    name="zozopdf",
    version=1.0,
    # can't get content of current path
    # long_description=Path(R".\README.md").read_text(),
    long_description="This is the homepage of our project.",
    # tests and data directory is not packages
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
