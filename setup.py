import os
from setuptools import setup, find_packages

VERSION = '1.0.0'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='crex',
	author='Matteo Romanello',
	author_email='matteo.romanello@gmail.com',
	url='http://github.com/mromanello/CRefEx/',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    #package_dir={'crex': 'crex'},
    package_data={'Crex': ['data/*.*']},
    long_description=read('README.md'),
    #install_requires=['partitioner','CRFPP'],
    zip_safe=False,
)
