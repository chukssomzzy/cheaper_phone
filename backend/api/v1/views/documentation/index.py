#!/usr/bin/env -S venv/bin/python3

status_specs = {
    "parameters": [],
    "definitions": {
        "status": {
            "type": "object",
            "title": "server status",
            "properties": {
                "status": {
                    "type": "string"
                }
            }
        }
    },
    "responses": {
        "200": {
            "description": "Get server status",
            "schema": {
                "$ref": "#/definitions/status"
            },
            "examples": {
                "status": "ok"
            }
        }
    }
}
stats_specs = {
    "parameters": [],
    "definitions": {
        "stats": {
            "type": "object",
            "title": "db stats",
            "properties": {
                "brand": {
                    "type": "string",
                },
                "category": {
                    "type": "string"
                },
                "product": {
                    "type": "string"
                },
                "user": {
                    "type": "string"
                }
            }
        }
    },
    "responses": {
        "200": {
            "description": "Get number of public db tables",
            "schema": {
                "$ref": "#/definitions/stats"
            }
        },
        "examples": {
            "brand": 100,
            "category": 20,
            "product": 1005,
        }
    }
}
