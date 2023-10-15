#!/usr/bin/env venv/bin/python3
"""Review endpoints documentation"""

from api.v1.utils.schemas.resolver import get_schema


get_product_review_spec = {
    "summary": "get review for a product",
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "required": True,
            "type": "string",
            "format": "uuid",
            "description": "user id for a user"
        },
        {
            "name": "product_id",
            "in": "path",
            "type": "string",
            "format": "uuid",
            "required": True,
            "description": "identifies the product to get it's review"
        },

    ],
    "definitions": {},
    "responses": {
        "200": {
            "description": "reviews for user",
            "schema": {
                "type": "object",
                "properties": {
                    "reviews": {
                        "type": "array",
                        "items": get_schema("review_schema.json")
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

post_product_review_spec = {
    "summary": "post a review for a product",
    "parameters": [
        {
            "type": "string",
            "format": "uuid",
            "name": "product_id",
            "description": "identifies the product to post it's review",
            "required": True,
            "in": 'path'
        },
        {
            "name": "reviews body in json",
            "required": True,
            "in": "body",
            "description": "contain review in json",
            "schema": get_schema("review_schema.json")
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
        "201": {
            "description": "id of successfully post review",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {
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

get_all_review_spec = {
    "summary": "get all reviews for a product",
    "parameters": [{
        "type": "string",
        "format": "uuid",
        "name": "product_id",
        "description": "identifies the product to post it's review",
        "required": True,
        "in": 'path'
    }],
    "definitions": {
        "review": {
            "type": "object",
            "properties": {
                "data": get_schema("review_schema.json"),
                "user": get_schema("customer_schema.json"),
            }
        },
        "reviews": {
            "type": "array",
            "items": {
                "$ref": "#/definitions/review"
            }
        }
    },
    "responses": {
        "200": {
            "description": "returns the rating with an array of reviews",
            "schema": {
                "type": "object",
                "properties": {
                    "rating": {
                        "type": "number",
                        "minimum": 0
                    },
                    "reviews": {
                        "$ref": "#/definitions/reviews"
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


delete_review_spec = {
    "summary": "delete a review by id",
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
        "204": {
            "description": "deleted product with product_id"
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}
