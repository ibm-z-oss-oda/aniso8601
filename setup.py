from setuptools import setup, find_packages

readme = open('README.rst', 'r')
README_TEXT = readme.read()
readme.close()

setup(
    name='aniso8601',
    version='4.0.2dev0',
    description='A library for parsing ISO 8601 strings.',
    long_description=README_TEXT,
    author='Brandon Nielsen',
    author_email='nielsenb@jetfuse.net',
    url='https://bitbucket.org/nielsenb/aniso8601',
    extras_require={
        'relative': ['python-dateutil>=2.7.3']
    },
    packages=find_packages(),
    test_suite='aniso8601.tests',
    tests_require=['mock>=2.0.0'],
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
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='iso8601 parser',
    project_urls={
        'Documentation': 'http://aniso8601.readthedocs.io/en/latest/',
        'Source': 'https://bitbucket.org/nielsenb/aniso8601',
        'Tracker': 'https://bitbucket.org/nielsenb/aniso8601/issues'
    }
)
