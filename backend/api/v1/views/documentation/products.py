#!/usr/bin/env venv/bin/python3
"""product endpoints"""
from api.v1.utils.schemas.resolver import get_schema

get_products_spec = {
    "tags": ["product"],
    "summary": "paginate products",
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "type": "string",
            "format": "byte",
            "required": False,
            "description": "authorizaton header token for customer only route"
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
        }
    ],
    "definitions": {
        "product_actions": {
            "type": "array",
            "items": {
                "type": "object"
            }
        },
        "actions": {
            "type": "object",
            "properties": {
                "order_by": {
                    "type": "string"
                }
            }
        },
        "product": {
            "type": "object",
            "description": "get product response",
            "properties": {
                "data": {
                    "type": "object",
                    "allOf": [
                        get_schema("products_schema.json")
                    ],
                    "properties": {
                        "image_url": {
                            "type": "string",
                            "format": "uri"
                        },
                        "url_key": {
                            "type": "string",
                            "format": "uri"
                        }
                    },
                    "unevaluatedProperties": False
                },
                "actions": {
                    "$ref": "#/definitions/product_actions"
                },
                "brands": get_schema("brand_schema.json"),
                "categories": {
                    "type": "array",
                    "items": get_schema("category_schema.json")
                }

            }
        }
    },
    "responses": {
        "200": {
            "description": "all products response",
            "schema": {
                "type": "object",
                "properties": {
                    "pagination": get_schema("pagination_schema.json"),
                    "actions": {
                        "$ref": "#/definitions/actions"
                    },
                    "products": {
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

get_product_by_id_spec = {
    "tags": ["product"],
    "summary": "Get a product by id",
    "parameters": [{
        "name": "Authorization",
        "in": "header",
        "type": "string",
        "format": "byte",
        "required": False,
        "description": "authorizaton header token for customer only route"
    }],
    "definitions": {
        "product_actions": {
            "type": "array",
            "items": {
                "type": "object",
            }
        }
    },
    "responses": {
        "200": {
            "description": "product",
            "schema": {
                "type": "object",
                "description": "get product response",
                "properties": {
                    "data": {
                        "type": "object",
                        "allOf": [
                            get_schema("products_schema.json")
                        ],
                        "properties": {
                            "image_url": {
                                "type": "string",
                                "format": "uri"
                            },
                            "url_key": {
                                "type": "string",
                                "format": "uri"
                            }
                        },
                        "unevaluatedProperties": False
                    },
                    "actions": {
                        "$ref": "#/definitions/product_actions"
                    },
                    "brands": get_schema("brand_schema.json"),
                    "categories": {
                        "type": "array",
                        "items": get_schema("category_schema.json")
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


post_product_spec = {
    "tags": ["product"],
    "summary": "post a product (role)",
    "parameters": [{
        "name": "Authorization",
        "in": "header",
        "type": "string",
        "format": "byte",
        "required": True,
        "description": "authorizaton header token for customer only route"
    },
        {
        "name": "product body",
        "in": "body",
        "required": True,
        "description": "product body in json",
        "schema": get_schema("products_schema.json")
    }],
    "definitions": {},
    "responses": {
        "200": {
            "description": "post product response",
            "schema": {
                "type": "object",
                "properties": {
                    "product": {
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

update_product_spec = {
    "tags": ["product"],
    "summary": "update a product (role)",
    "parameters": [{
        "name": "Authorization",
        "in": "header",
        "type": "string",
        "format": "byte",
        "required": True,
        "description": "authorizaton header token for customer only route"
    },
        {
        "name": "product body",
        "in": "body",
        "required": True,
        "description": "product body in json",
        "schema": get_schema("product_update_schema.json")
    }],
    "definitions": {},
    "responses": {
        "200": {
            "description": "update a product response",
            "schema": get_schema("products_schema.json")
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}

delete_product_spec = {
    "tags": ["product"],
    "summary": "delete a product (role)",
    "parameters": [{
        "name": "Authorization",
        "in": "header",
        "type": "string",
        "format": "byte",
        "required": True,
        "description": "authorizaton header token for customer only route"
    }],
    "definitions": {},
    "responses": {
        "200": {
            "description": "delete a product by id"
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}
