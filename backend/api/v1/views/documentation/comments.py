#!/usr/bin/env -S venv/bin/python3
"""documentations for comment endpoints"""

from api.v1.utils.schemas.resolver import get_schema


get_comments_spec = {
    "tags": ["comment"],
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
            "name": "product_id",
            "in": "path",
            "type": "string",
            "format": "uuid",
            "required": True,
            "description": "identifies the product to get from db by id"
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
        "comment_data": {
            "type": "object",
            "title": "comments object and user",
            "properties": {
                "data": get_schema("comment_schema.json"),
                "user": get_schema("customer_schema.json")
            }
        },
        "comments": {
            "type": "array",
            "description": "contains all comment_data",
            "items": {
                "$ref": "#/definitions/comment_data"
            }
        }
    },
    "responses": {
        "200": {
            "description": "get all comment for a product",
            "schema": {
                "type": "object",
                "properties": {
                    "comments": {
                        "$ref": "#/definitions/comments"
                    },
                    "pagination": get_schema("pagination_schema.json"),
                    "actions": {
                        "$ref": "#/definitions/actions"
                    }
                }
            }
        },
        "404": {
            "description": "product not found in db with the product_id",
            "examples": {
                "message": "product with product_id d00c714b-7600-4d04-9730-fe364f520be5, not found"
            }
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}

post_comment_spec = {
    "tags": ["comment"],
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
            "description": "product identifier string",
            "type": "string",
            "format": "uuid",
            "required": True,
            "name": "product_id"
        }
    ],
    "definitions": {
    },
    "responses": {
        "200": {
            "schema": {
                "type": "object",
                "title": "return value",
                "properties": {
                    "id": {
                        "description": "uuid for the newly created comment",
                        "type": "string"
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


delete_comment_spec = {
    "tags": ["comment"],
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "type": "string",
            "required": True,
            "description": "authorizaton header token for customer only route"
        },
        {
            "name": "product_id",
            "in": "path",
            "type": "string",
            "format": "uuid",
            "required": True,
            "description": "identifies the product to get from db by id"
        }
    ],
    "definitions": {},
    "responses": {
        "204": {
            "description": "no response"
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}
