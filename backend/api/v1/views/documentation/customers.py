#!/usr/bin/env venv/bin/python3

"""Defines openapi specs for customer endpoints"""

from api.v1.utils.schemas.resolver import get_schema


create_customer_specs = {
    "parameters": [
        {
            "name": "customer data",
            "in": "body",
            "description": "customer information",
            "required": True,
            "schema": get_schema("customer_schema.json")
        }
    ],
    "definitions": {
        "return_value": {
            "title": "return status from register route",
            "type": "string",
            "properties": {
                "customer": {
                    "type": "string",
                    "format": "uuid"
                }
            }

        },
    },
    "responses": {
        "201": {
            "description": "Register a new customer to db",
            "schemas": {
                "$ref": "#/definitions/return_value"
            },
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}

customer_login_specs = {
    "parameters": [],
    "definitions": {
        "login_token": {
            "type": "object",
            "title": "contains access token and refresh token for the login user",
            "properties": {
                "access_token": {
                    "type": "string",
                },
                "refresh_token": {
                    "type": "string"
                }
            }
        }
    },
    "responses": {
        "200": {
            "description": "returns access and refresh token when successfully login",
            "schema": {
                "$ref": "#/definitions/login_token"
            },
        },
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        }
    }
}


refresh_spec = {
    "parameters": [
        {
            "in": "header",
            "description": "authorization header",
            "required": True,
            "name": "Authorization",
            "type": "string",
        },
    ],
    "definitions": {
        "access_token": {
            "type": "object",
            "title": "access token for the login user",
            "properties": {
                "access_token": {
                    "type": "string"
                }
            }
        }
    },
    "responses": {
        "200": {
            "description": "returns an object containing the access token",
            "schema": {
                "$ref": "#/definitions/access_token"
            },
            "examples": {
                "access_token": "<access_token>"
            }
        }
    }
}

profile_specs = {
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "type": "string",
            "required": True,
            "description": "authorizaton header token for customer only route"
        }
    ],
    "definitions": {
        "actions": {
            "type": "object",
            "title": "actions that can be performed by a user on his profile",
            "properties": {
                "editUser": {
                    "type": "string",
                    "format": "uri"
                },
                "changePassword": {
                    "type": "string",
                    "format": "uri"
                },
                "getUserCart": {
                    "type": "string",
                    "format": "uri"
                },
            }
        }
    },
    "responses": {
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        },
        "200": {
            "description": "profile information for a user",
            "schema": {
                "type": "object",
                "properties": {
                    "actions": {
                        "$ref": "#/definitions/actions"
                    },
                    "customer": {
                        "type": "object",
                        "title": "contains customer information",
                        "properties": {
                            "data": get_schema("customer_schema.json"),
                            "shipping_address": get_schema("shipping_address_schema.json")
                        }
                    }
                }
            }
        }
    }
}


update_customer_spec = {
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "type": "string",
            "required": True,
            "description": "authorizaton header token for customer only route"
        },
        {
            "name": "customer information",
            "in": "body",
            "required": True,
            "description": "body of request containing customer information to update",
            "schema": get_schema("update_profile_schema.json")
        }
    ],
    "definitions": {},
    "responses": {
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        },
        "200": {
            "descripton": "contains updated customer information",
            "schema": get_schema("update_profile_schema.json")
        }
    }
}

change_password_spec = {
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "type": "string",
            "required": True,
            "description": "authorizaton header token for customer only route"
        },
        {
            "name": "change password data",
            "in": "body",
            "required": True,
            "description": "new_password and old_password string",
            "schema": get_schema("change_password_schema.json")
        }
    ],
    "definitions": {},
    "responses": {
        "default": {
            "description": "error payload",
            "schema": get_schema("error_model_schema.json")
        },
        "204": {
            "description": "no content",
        }

    }
}
