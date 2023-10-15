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
    "definitions": {
        "cart_items": {
            "type": "object",
            "description": "single item in a cart",
            "properties": {
                "data": get_schema("cart_item_detail_schema.json"),
                "product": get_schema("products_schema.json")
            }
        }
    },
    "responses": {
        "200": {
            "description": "return a cart and all product in the cart",
            "schema": {
                "type": "object",
                "title": "response object",
                "properties": {
                    "data": get_schema("cart_schema.json"),
                    "items": {
                        "type": "array",
                        "description": "object contained in cart",
                        "items": {
                            "$ref": "#/definitions/cart_items"
                        }
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

add_product_to_cart_spec = {
    "summary": "add product to cart",
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "type": "string",
            "format": "byte",
            "required": True,
            "description": "authorizaton header token for customer only route"
        },
        {
            "name": "product_id",
            "descripion": "string identifier for category",
            "minimum": 0,
            "required": True,
            "in": "path",
            "type": "string",
            "format": "uuid"
        }
    ],
    "definitions": {},
    "responses": {
        "200": {
            "description": "responds with customer and cart",
            "schema": {
                "type": "object",
                "title": "response",
                "properties": {
                    "customer": get_schema("customer_schema.json"),
                    "cart": {
                        "type": "object",
                        "properties": {
                            "data": get_schema("cart_schema.json"),
                            "items": {
                                "type": "array",
                                "items": get_schema("cart_item_detail_schema.json")
                            }
                        }
                    }
                }
            }
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    },
}


remove_product_from_cart_spec = {
    "summary": "Remove a product from cart",
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "type": "string",
            "format": "byte",
            "required": True,
            "description": "authorizaton header token for customer only route"
        },
        {
            "name": "product_id",
            "descripion": "string identifier for category",
            "minimum": 0,
            "required": True,
            "in": "path",
            "type": "string",
            "format": "uuid"
        }
    ],
    "definitions": {},
    "responses": {
        "200": {
            "description": "responds with customer and cart",
            "schema": {
                "type": "object",
                "title": "response",
                "properties": {
                    "customer": get_schema("customer_schema.json"),
                    "cart": {
                        "type": "object",
                        "properties": {
                            "data": get_schema("cart_schema.json"),
                            "items": {
                                "type": "array",
                                "items": get_schema("cart_item_detail_schema.json")
                            }
                        }
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

delete_from_cart_spec = {
    "summary": "deletes a product from cart if exits",
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "type": "string",
            "format": "byte",
            "required": True,
            "description": "authorizaton header token for customer only route"
        },
        {
            "name": "product_id",
            "descripion": "string identifier for category",
            "minimum": 0,
            "required": True,
            "in": "path",
            "type": "string",
            "format": "uuid"
        }
    ],
    "definitions": {},
    "responses": {
        "204": {
            "description": "successfully deleted product"
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    },
}
