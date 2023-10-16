#!/usr/bin/env -S venv/bin/python3
"""Promotions endpoints"""

from api.v1.utils.schemas.resolver import get_schema

get_product_promotions_spec = {
    "tags": ["promotion"],
    "summary": 'get all product promotions',
    "parameters": [
        {
            "name": "product_id",
            "format": "uuid",
            "in": "path",
            "required": True,
            "description": "product id to get its promotions"
        }
    ],
    "definitions": {
    },
    "responses": {
        "200": {
            "description": "promtions for the product",
            "schema": {
                "type": "array",
                "items": get_schema("promotion_schema.json")
            }
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}

post_promotions_spec = {
    "tags": ["promotion"],
    "summary": "post a promotion",
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
            "name": "promotions",
            "in": "body",
            "required": True,
            "description": "promotions body",
            "schema": get_schema("promotion_schema.json")
        }
    ],
    "definitions": {},
    "responses": {
        "201": {
            "description": "promotions created",
            "schema": get_schema("promotion_schema.json")
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}

delete_promotion_spec = {
    "tags": ["promotion"],
    "summary": "delete a promotions",
    "parameters": [{
        "name": "Authorization",
        "in": "header",
        "type": "string",
        "format": "byte",
        "required": True,
        "description": "authorizaton header token for customer only route"
    }],
    "definition": {},
    "responses": {
        "204": {
            "description": "deleted promotion"
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}

get_product_by_promotions = {
    "tags": ["promotion"],
    "summary": "get a promotion products",
    "parameters": [{
        "in": "header",
        "description": "authorization header",
        "required": True,
        "format": "byte",
        "name": "Authorization",
        "type": "string",
    },
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
    }],
    "definitions": {
        "products": {
            "type": "array",
            "items": get_schema("products_schema.json")
        }
    },
    "responses": {
        "200": {
            "description": "get all product with promotion identified by product_id",
            "schema": {
                "type": "object",
                "properties": {
                    "pagination": get_schema("pagination_schema.json"),
                    "products": "#/definitions/products"
                }
            }
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}

get_promotions_spec = {
    "tags": ["promotion"],
    "summary": "get all promotions paginating them",
    "parameters": [{
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
    }],
    "definitions": {
        "promotion": {
            "type": "object",
            "properties": {
                "data": get_schema("promotion_schema.json"),
                "actions": {
                    "type": "array",
                    "items": {
                        "type": "object"
                    }
                }
            }
        }
    },
    "responses": {
        "200": {
            "description": "get all promotions paginated",
            "schema": {
                "type": "object",
                "properties": {
                    "pagination": get_schema("pagination_schema.json"),
                    "promotions": {
                        "type": "array",
                        "items": {
                            "$ref": "#/definitions/product"
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

add_promotion_product_spec = {
    "tags": ["promotion"],
    "summary": "add a promotion to a product",
    "parameters": [
        {
            "in": "header",
            "description": "authorization header",
            "required": True,
            "format": "byte",
            "name": "Authorization",
            "type": "string",
        },
        {
            "name": "promotion_id",
            "in": "path",
            "required": True,
            "description": "identifies the promotion to add to product",
            "type": "number",
            "minimum": 0
        },
        {
            "name": "product_id",
            "in": "path",
            "required": True,
            "description": "identifies the product the promotion should be added to",
            "type": "string",
            "format": "string"
        }
    ],
    "definitions": {},
    "responses": {
        "200": {
            "description": "promotion successfully added to product",
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}

delete_promotion_product_spec = {
    "tags": ["promotion"],
    "summary": "remove a promotion from a product",
    "parameters": [
        {
            "in": "header",
            "description": "authorization header",
            "required": True,
            "format": "byte",
            "name": "Authorization",
            "type": "string",
        },
        {
            "name": "promotion_id",
            "in": "path",
            "required": True,
            "description": "identifies the promotion to add to product",
            "type": "number",
            "minimum": 0
        },
        {
            "name": "product_id",
            "in": "path",
            "required": True,
            "description": "identifies the product the promotion should be added to",
            "type": "string",
            "format": "string"
        }
    ],
    "definitions": {},
    "responses": {
        "204": {
            "description": "promotion successfully removed from product"
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}

update_promotion_spec = {
    "tags": ["promotion"],
    "summary": "update a promotion",
    "parameters": [{
        "in": "header",
        "description": "authorization header",
        "required": True,
        "format": "byte",
        "name": "Authorization",
        "type": "string",
    },
        {
            "name": "promotion_id",
            "in": "path",
            "required": True,
            "description": "identifies the promotion to add to product",
            "type": "number",
            "minimum": 0
    }],
    "definitions": {},
    "responses": {
        "200": {
            "description": "updated promotion",
            "schema": get_schema("promotion_schema.json")
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}
