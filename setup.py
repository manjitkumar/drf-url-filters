from setuptools import setup
import os
import sys
sys.path.insert(0, '.')

try:
    import atexit
    import pypandoc
    README = pypandoc.convert('README.md', 'rst', 'markdown')
    with open('README.rst', 'w') as f:
        f.write(README)
    atexit.register(lambda: os.unlink('README.rst'))
except (ImportError, OSError):
    print('WARNING: Could not locate pandoc, using Markdown README.')
    with open('README.md') as f:
        README = f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

__name__ = 'drf-url-filters'
__version__ = '0.5.1'
__author__ = 'Manjit Kumar'
__author_email__ = 'manjit1727@gmail.com'
__url__ = 'https://github.com/manjitkumar/drf-url-filters'
__download_url__ = 'https://github.com/manjitkumar/drf-url-filters/archive/v0.1.3.tar.gz'


setup(
    name=__name__,
    version=__version__,
    packages=['filters'],
    include_package_data=True,
    description=(
        'A django app to apply filters on drf querysets '
        'using query params with validations using voluptuous.'
    ),
    long_description=README,
    url=__url__,
    download_url=__download_url__,
    author=__author__,
    author_email=__author_email__,
    install_requires=[
        'Django>=1.8.11',
        'djangorestframework>=3.3.3',
        'voluptuous>=0.8.10',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='drf-url-filters, filters, queryparameters',
    test_suite='nose2.collector.collector',
    tests_require=['nose2'],
)
