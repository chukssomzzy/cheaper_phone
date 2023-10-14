#!/usr/bin/env venv/bin/python3
"""Contains all endpoint related to user cart"""
from api.v1.utils.schemas.resolver import get_schema


get_cart_spec = {
    "summary": "Get a cart linked to the login customer",
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "type": "string",
            "format": "byte",
            "required": True,
            "description": "authorizaton header token for customer only route"
        }
    ],
    "definitions": {},
    "responses": {
        "200": {
            "description": "return a cart and all product in the cart",
            "schema": {
                "type": "object",
                "title": "response object",
                "properties": {
                    "items": {
                        "type": "array",
                        "description": "object contained in cart",
                        "items": get_schema("products_schema.json")
                    }
                }
            }
        }
    }
}
