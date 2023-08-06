#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import setuptools
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
long_description = ""
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="py-gql-client",
    version="1.0.1",
    author="Facebook Inc.",
    description="Python GraphQL generated code client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include=["gql_client", "gql_client.*"]),
    license="BSD License",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    scripts=["bin/gql-compiler"],
    install_requires=[
        "gql>=v3.0.0a5",
        "dataclasses==0.6",
        "dataclasses-json==0.5.2",
    ],
)
