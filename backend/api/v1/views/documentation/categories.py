#!/usr/bin/env -S venv/bin/python3
"""documents categories endpoints"""

from api.v1.utils.schemas.resolver import get_schema


get_categories_schema = {
    "tags": ["categories"],
    "parameters": [
        {
            "name": "order_by",
            "type": "string",
            "in": "query",
            "required": False,
            "description": "describes what to key to sort response with"
        },
        {
            "name": "page",
            "description": "defines the current page to get from db",
            "required": False,
            "in": "query",
            "type": "number",
            "minimum": 0
        },
        {
            "name": "limit",
            "type": "number",
            "required": False,
            "in": "query",
            "minimum": 0,
            "description": "defines the number of object in a page"
        }
    ],
    "definitions": {
        "actions": {
            "type": "object",
            "title": "describes action that can be performed for a order",
            "properties": {
                "order_by": {
                    "descripton": "shows the keys the response can be order with",
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        },
        "category": {
            "type": "object",
            "title": "category objects",
            "properties": {
                "actions": {
                    "description": "action performable by category",
                    "type": "array",
                    "items": {
                        "description": "categories actions",
                        "type": "string"
                    }
                },
                "data": get_schema("category_schema.json")
            }
        },
        "categories": {
            "description": "list of category object",
            "type": "array",
            "items": {
                "$ref": "#/definitions/category"
            }
        }
    },
    "responses": {
        "200": {
            "descriptions": "paginate and returns all categories",
            "schema": {
                "type": "object",
                "title": "response object for get categories",
                "properties": {
                        "pagination": get_schema("pagination_schema.json"),
                        "categories": {
                            "$ref": "#/definitions/categories"
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


get_product_by_category_spec = {
    "tags": ["categories"],
    "parameters": [
        {
            "name": "order_by",
            "type": "string",
            "in": "query",
            "required": False,
            "description": "describes what to key to sort response with"
        },
        {
            "name": "page",
            "description": "defines the current page to get from db",
            "required": False,
            "in": "query",
            "type": "number",
            "minimum": 0
        },
        {
            "name": "limit",
            "type": "number",
            "required": False,
            "in": "query",
            "minimum": 0,
            "description": "defines the number of object in a page"
        },
        {
            "description": "category integer identifier",
            "name": "category_id",
            "in": "path",
            "required": True,
            "type": "number",
            "minimum": 0,
        }
    ],
    "definitions": {

    },
    "responses": {
        "200": {
            "description": "response object for product by category",
            "schema": {
                "type": "object",
                "description": "response object schema",
                "properties": {
                    "category": get_schema("category_schema.json"),

                }
            }
        }
    }
}

post_category_spec = {
    "tags": ["categories"],
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "type": "string",
            "required": True,
            "format": "byte",
            "description": "authorizaton header token for customer only route"
        },
        {
            "name": "category body",
            "in": "body",
            "required": True,
            "description": "category data",
            "schema": get_schema("category_schema.json")
        }
    ],
    "definitions": {},
    "responses": {
        "200": {
            "description": "post a category if user is admin",
            "schema": {
                "type": "object",
                "title": "return id of newly created category",
                "properties": {
                    "category": {
                        "type": "string",
                        "format": "uuid"
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

delete_category_spec = {
    "tags": ["categories"],
    "parameters": [
        {
            "name": "category_id",
            "descripion": "integer identifier for category",
            "minimum": 0,
            "required": True,
            "in": "path",
            "type": "number"
        }
    ],
    "definitions": {},
    "responses": {
        "204": {
            "description": "no response when successfully deleted",
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}
