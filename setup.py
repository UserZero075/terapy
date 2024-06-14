from setuptools import setup


fld = open("./README.md")
long_description = fld.read()
fld.close()

setup(
    name="terapy",
    version="0.1.3",
    description="A library to download from terabox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Diego Alberto Barreiro Delgado",
    author_email="rockstarcu.dev@gmail.com",
    url="https://github.com/RockstarDevCuba/terapy",
    install_requires=[
        'yarl>=1.9.4',
        'httpx>=0.27.0',
        'multidict>=6.0.5',
    ],
    packages="terapy"
)