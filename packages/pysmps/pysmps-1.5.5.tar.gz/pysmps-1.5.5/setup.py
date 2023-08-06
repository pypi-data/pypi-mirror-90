from setuptools import setup, find_packages

with open('requirements.txt', "r") as reader:
    required = reader.read().splitlines()

with open("PYPI_README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name='pysmps',
    version='1.5.5',
    description='Utilities for parsing MPS and SMPS file formats.',
	long_description=readme,
	long_description_content_type="text/markdown",
    author='Julian Maerte',
    author_email='maertej@students.uni-marburg.de',
    packages=find_packages(),
	url="https://github.com/jmaerte/pysmps",
	install_required=required,
)
