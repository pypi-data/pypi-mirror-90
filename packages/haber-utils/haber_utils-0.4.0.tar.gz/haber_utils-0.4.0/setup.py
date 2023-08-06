# Author: Ron Haber
# Date: 3.1.2021

from setuptools import find_packages, setup

with open("README.md", 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='haber_utils',
    packages=find_packages(include=['haber_utils']),
    version='0.4.0',
    description='General utility functions that keep being rewritten',
    author='Ron Haber',
    author_email='ron.haber@hotmail.com',
    license='MIT',
    install_requires=['pandas'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/haberrj/utilities_library',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.4',
)