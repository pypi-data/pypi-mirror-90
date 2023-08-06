
from setuptools import setup
from setuptools import find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = 'fundamentus',
    packages = find_packages(where='src'),
    package_dir = {'': 'src'},

    version='0.0.0.0',

    scripts=[
        'bin/fundamentus.csv.py',
        'bin/magic_formula.simple.py',
    ],

    url='https://github.com/mv/fundamentus/',
    description='Fundamentus: API to download data from the site https://www.fundamentus.com.br/',
    long_description=long_description,
    long_description_content_type="text/markdown",

    author='Mv - Marcus Vinicius Ferreira',
    author_email='ferreira.mv@gmail.com',

    install_requires=[
       'requests >= 2.25.1',
       'requests-cache >= 0.5.2',
       'pandas >= 1.1.5',
       'lxml >= 4.6.2',
       'tabulate >= 0.8.7',
    ],

)


