from setuptools import setup, find_packages

VERSION = '0.2'
LONG_DESC = """
CRefEx is a tool for the automatic extraction of Canonical References.
"""

setup(name='crex',
	author='Matteo Romanello',
	author_email='matteo.romanello@gmail.com',
	url='http://github.com/mromanello/CRefEx/',
    version=VERSION,
    packages=find_packages(),
    package_data={'crex': ['data/*']},
    long_description=LONG_DESC,
    install_requires=['partitioner,CRFPP'],
    zip_safe=False,
)
