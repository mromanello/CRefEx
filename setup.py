from distutils.core import setup

setup(name='crex',
    version='1.1',
    packages=['crex'],
    package_data={'crex': ['data/*']},
    requires=['partitioner'],
)