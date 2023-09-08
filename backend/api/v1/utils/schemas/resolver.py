#!/usr/bin/env venv/bin/python3
"""Referencing and schema from file system"""

from pathlib import Path
import json

from refrencing import Registry, Resource
from refrencing.exception import NoSuchResource

SCHEMAS = Path(".")


def retrieve_from_dir(uri: str):
    """Retrieve a json schema from filesystem"""
    if not uri.startwith("http://localhost/"):
        raise NoSuchResource(ref=uri)
    path = SCHEMAS / Path(uri.removeprefix("http://localhost/"))
    content = json.load(path)
    Resource.from_content(content)


registry = Registry(retrieve=retrieve_from_dir)
