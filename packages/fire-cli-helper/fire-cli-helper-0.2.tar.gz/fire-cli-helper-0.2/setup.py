from setuptools import setup, find_packages
from os import path

# https://packaging.python.org/guides/making-a-pypi-friendly-readme/
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fire-cli-helper',
    version=0.2,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/frogrammer/fire-cli-helper',
    author='Luke Vinton',
    author_email='luke0vinton@gmail.com',
    license='Apache 2.0',
    packages=find_packages(),
    install_requires=['fire'],
    tests_require=[],
    classifiers=[],
    test_suite='',
    entry_points={
        'console_scripts': [
            'firehelper_example = example_cli.__main__:main',
        ],
    },
)
