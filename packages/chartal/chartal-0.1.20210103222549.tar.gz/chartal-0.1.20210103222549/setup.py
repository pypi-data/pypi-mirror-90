import pathlib
from setuptools import setup, find_packages

import datetime
currentDT = datetime.datetime.now()

#Setup Path
HERE = pathlib.Path(__file__).parent

#Readme file data
README = (HERE / "README.md").read_text()


setup(
    name = 'chartal',
    version = '0.1.'+currentDT.strftime("%Y%m%d%H%M%S"),
    packages = find_packages(exclude=("tests",)),
    description="",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Adam Blacke",
    author_email="adamblacke@gmail.com",
)