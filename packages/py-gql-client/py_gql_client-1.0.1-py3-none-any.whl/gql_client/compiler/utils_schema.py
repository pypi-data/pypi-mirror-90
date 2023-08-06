#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import glob
from enum import Enum
import json
import os
import requests
from typing import Tuple

from graphql import (
    build_ast_schema,
    build_client_schema,
    get_introspection_query,
    GraphQLSchema,
)
from graphql.language.parser import parse
from graphql.language import OperationDefinitionNode, FragmentDefinitionNode
from graphql.language.ast import DocumentNode


class QueryType(Enum):
    OPERATION = 1
    FRAGMENT = 2


def load_introspection_from_server(url):
    query = get_introspection_query()
    request = requests.post(url, json={"query": query})
    if request.status_code == 200:
        return request.json()["data"]

    raise Exception(
        f"Request failure with {request.status_code} status code for query {query}"
    )


def load_introspection_from_file(filename):
    with open(filename, "r") as fin:
        return json.load(fin)


def load_schema(uri):
    introspection = (
        load_introspection_from_file(uri)
        if os.path.isfile(uri)
        else load_introspection_from_server(uri)
    )
    return build_client_schema(introspection)


def compile_schema_library(schema_library: str) -> GraphQLSchema:
    full_schema = ""
    # use the following line to use .graphqls files as well
    # os.path.join(schema_library, "**/*.graphql*"), recursive=True
    schema_filepaths = glob.glob(
        os.path.join(schema_library, "**/*.graphql"), recursive=True
    )
    for schema_filepath in schema_filepaths:
        with open(schema_filepath) as schema_file:
            full_schema = full_schema + schema_file.read()
    return build_ast_schema(parse(full_schema))


def get_query_details(document_ast: DocumentNode) -> Tuple[str, QueryType]:
    definitions = document_ast.definitions
    assert (
        len(definitions) == 1
    ), f"number of definitions in query is invalid: {len(definitions)}"
    definition = definitions[0]
    if isinstance(definition, OperationDefinitionNode):
        if not definition.name:
            raise AssertionError("operation has no name")
        return (definition.name.value, QueryType.OPERATION)
    elif not isinstance(definition, FragmentDefinitionNode):
        raise AssertionError("invalid definition")
    return (definition.name.value, QueryType.FRAGMENT)
