#!/usr/bin/env venv/bin/python3
"""Referencing and schema from file system"""

from pathlib import Path
import json

from referencing import Registry, Resource
from referencing.exceptions import NoSuchResource

SCHEMAS = Path(__file__).parent


def retrieve_from_dir(uri: str):
    """Retrieve a json schema from filesystem"""
    schema_path = SCHEMAS / uri
    content = json.loads(schema_path.read_text())
    return Resource.from_contents(content)


registry = Registry(retrieve=retrieve_from_dir)
