"""Setup configuration and dependencies for pystonkslib."""

from os import path

from setuptools import find_packages, setup

with open("requirements.txt") as req_file:
    REQUIREMENTS = req_file.readlines()


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

COMMANDS = [
    "example_command=pystonkslib.example:main",
    "pslib=pystonkslib.tools.pslib:main",
]

setup(
    name="pystonkslib",
    version="0.0.5",
    author="Micheal Taylor",
    author_email="bubthegreat@gmail.com",
    url="https://gitlab.com/bubthegreat/pystonkslib",
    include_package_data=True,
    description="This is a stonks data pulling library",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={"": "src",},
    python_requires=">=3.6.6",
    entry_points={"console_scripts": COMMANDS},
    install_requires=REQUIREMENTS,
)
