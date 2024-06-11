from setuptools import setup,find_packages


fld = open("./README.md")
long_description = fld.read()
fld.close()

filerequired = open("./requirements.txt")
required = filerequired.readlines()
filerequired.close()

setup(
    name="terapy",
    version="0.1.0",
    description="A library to download from terabox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Diego Alberto Barreiro Delgado",
    author_email="rockstarcu.dev@gmail.com",
    url="https://github.com/RockstarDevCuba/terapy",
    requires=required,
    package=find_packages()
)