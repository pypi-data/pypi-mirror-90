"""Setup.py."""
from setuptools import setup, find_packages

setup(
    name='fire-cli-helper',
    version=0.1,
    description='',
    url='',
    author='Luke Vinton',
    author_email='luvinton@microsoft.com',
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
