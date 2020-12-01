import sys

from aniso8601 import __version__
from os import path
from setuptools import setup, find_packages

TESTS_REQUIRE = []

#Mock is only required for Python 2
PY2 = sys.version_info[0] == 2

if PY2:
    TESTS_REQUIRE.append('mock>=2.0.0')

THIS_DIRECTORY = path.abspath(path.dirname(__file__))
with open(path.join(THIS_DIRECTORY, 'README.rst'), encoding='utf-8') as f:
    README_TEXT = f.read()

setup(
    name='aniso8601',
    version=__version__,
    description='A library for parsing ISO 8601 strings.',
    long_description=README_TEXT,
    author='Brandon Nielsen',
    author_email='nielsenb@jetfuse.net',
    url='https://bitbucket.org/nielsenb/aniso8601',
    packages=find_packages(),
    test_suite='aniso8601',
    tests_require=TESTS_REQUIRE,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='iso8601 parser',
    project_urls={
        'Documentation': 'https://aniso8601.readthedocs.io/',
        'Source': 'https://bitbucket.org/nielsenb/aniso8601',
        'Tracker': 'https://bitbucket.org/nielsenb/aniso8601/issues'
    }
)
