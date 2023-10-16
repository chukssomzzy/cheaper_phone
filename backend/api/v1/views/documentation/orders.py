#!/usr/bin/env venv/bin/python3
"""Orders endpoints"""
from api.v1.utils.schemas.resolver import get_schema


get_user_orders_spec = {
    "tags": ["order"],
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
        "orders": {
            "type": "array",
            "description": "orders by a user",
            "items": {
                    "type": "object",
                    "title": "order item",
                    "properties": {
                        "order": {
                            "$ref": "#/definitions/order"
                        }
                    }
            }
        },
        "order": {
            "type": "object",
            "properties": {
                "data": get_schema("order_schema.json"),
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "data": get_schema("order_item_schema.json"),
                            "product": get_schema("products_schema.json")
                        }
                    }
                },
                "address": get_schema("shipping_address_schema.json")
            }
        }
    },
    "responses": {
        "200": {
            "description": "paginated orders response",
            "schema": {
                "type": "object",
                "title": "orders response",
                "properties": {
                    "pagination": get_schema("pagination_schema.json"),
                    "actions": {
                        "$ref": "#/definitions/actions"
                    },
                    "orders": {
                        "$ref": "#/definitions/orders"
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

create_order_spec = {
    "tags": ["order"],
    "summary": "create an order from cart content",
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
            "description": "string cart identifier",
            "name": "cart_id",
            "in": "path",
            "format": "uuid",
            "type": "string",
            "required": True
        }
    ],
    "definitions": {},
    "responses": {
        "201": {
            "description": "create order response",
            "schema": {
                "type": "object",
                "properties": {
                    "order": {
                        "type": "number",
                        "minimum": 0
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

get_order_by_id_spec = {
    "tags": ["order"],
    "summary": "get an order by its id",
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
            "type": "number",
            "name": "order_id",
            "description": "integer identifier for order",
            "in": "path",
            "required": True,
            "minimum": 0
        }
    ],
    "definitions": {
        "actions": {
            "type": "object",
            "title": "actions performable on orders",
            "properties": {
                "cancelOrder": {
                    "type": "string",
                    "format": "uri"
                }
            }
        }
    },
    "responses": {
        "200": {
            "description": "order",
            "schema": {
                "type": "object",
                "properties": {
                    "actions": {
                        "$ref": "#/definitions/actions"
                    },
                    "status": {
                        "type": "string"
                    },
                    "data": get_schema("order_schema.json")
                }
            }
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}


def return_order_spec(summary):
    """Return order spec for admin route"""

    return (
        {
            "tags": ["order"],
            "summary": summary,
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
                    "type": "number",
                    "name": "order_id",
                    "description": "integer identifier for order",
                    "in": "path",
                    "required": True,
                    "minimum": 0
                }
            ],
            "definitions": {},
            "responses": {
                "200": {
                    "description": "response",
                    "schema": get_schema("order_schema.json")
                },
                "default": {
                    "description": "error payload",
                    "schema": get_schema("error_model_schema.json")
                }
            }
        }
    )
