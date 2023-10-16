#!/usr/bin/env -S venv/bin/python3
"""Shippping Address endpoints documentation"""

from api.v1.utils.schemas.resolver import get_schema

post_address_spec = {
    "tags": ["shipping address"],
    "summary": "Post a shipping address for a user",
    "parameters": [
        {
            "in": "header",
            "description": "authorization header",
            "required": True,
            "format": "byte",
            "name": "Authorization",
            "type": "string",
        }
    ],
    "definitions": {},
    "responses": {
        "201": {
            "description": "all customer address",
            "schema": {
                "type": "object",
                "properties": {
                    "addresses": {
                        "type": "array",
                        "items": get_schema("shipping_address_schema.json")
                    }
                }
            }
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}

get_all_address_spec = {
    "tags": ["shipping address"],
    "summary": "Get all shipping address for a user",
    "parameters": [
        {
               "in": "header",
               "description": "authorization header",
               "required": True,
               "format": "byte",
               "name": "Authorization",
               "type": "string",
        }
    ],
    "definitions": {},
    "responses": {
        "200": {
            "description": "all customer address",
            "schema": {
                "type": "object",
                "properties": {
                    "addresses": {
                           "type": "array",
                           "items": get_schema("shipping_address_schema.json")
                    }
                }
            }
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}


delete_address_spec = {
    "tags": ["shipping address"],
    "summary": "delete a address",
    "parameters": [
        {
            "name": "address_id",
            "type": "number",
            "description": "identifies an address",
            "required": True,
            "in": "path",
            "minimum": 0
        },
        {
            "in": "header",
            "description": "authorization header",
            "required": True,
            "format": "byte",
            "name": "Authorization",
            "type": "string",
        }
    ],
    "definitions": {},
    "responses": {
        "204": {
            "description": "address deleted"
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}


update_address_spec = {
    "tags": ["shipping address"],
    "summary": "update a customer address",
    "parameters": [
        {
            "name": "address_id",
            "type": "number",
            "description": "identifies an address",
            "required": True,
            "in": "path",
            "minimum": 0
        },
        {
            "in": "header",
            "description": "authorization header",
            "required": True,
            "format": "byte",
            "name": "Authorization",
            "type": "string",
        },
        {
            'name': "shipping address json",
            "description": "shipping address json",
            "in": "body",
            "required": True,
            "schema": get_schema("update_shipping_address_schema.json")
        }
    ],
    "definitions": {},
    "responses": {
        "200": {
            "description": "returns update shipping address",
            "schema": get_schema("shipping_address_schema.json")
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}

get_address_by_id_spec = {
    "tags": ["shipping address"],
    "summary": "Get a shipping address",
    "parameters": [
        {
            "name": "address_id",
            "type": "number",
            "description": "identifies an address",
            "required": True,
            "in": "path",
            "minimum": 0
        },
        {
            "in": "header",
            "description": "authorization header",
            "required": True,
            "format": "byte",
            "name": "Authorization",
            "type": "string",
        }
    ],
    "definitions": {},
    "responses": {
        "200": {
            "description": "responds with a shipping address",
            "schema": get_schema("shipping_address_schema.json")
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}
