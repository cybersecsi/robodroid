"""
  This module contains the schemas (for YAML files currently) that will be validated with 'cerberus'
"""

config_tpl_lib_schema = {
    "id": {
        "type": "string",
        "required": True,
    },
    "info": {
        "type": "dict",
        "required": True,
        "schema": {
            "package-name": {
                "type": "string",
                "required": True,
            },
            "description": {
                "type": "string",
                "required": True,
            },
        },
    },
    "inputs": {
        "type": "list",
        "required": True,
        "schema": {
            "type": "dict",
            "required": True,
            "schema": {
                "id": {
                    "type": "string",
                    "required": True,
                },
                "description": {
                    "type": "string",
                    "required": True,
                },
            },
        },
    },
}

config_lib_schema = {
    "id": {
        "type": "string",
        "required": True,
    },
    "inputs": {
        "type": "list",
        "required": True,
        "schema": {
            "type": "dict",
            "required": True,
            "schema": {
                "id": {
                    "type": "string",
                    "required": True,
                },
                "value": {
                    "type": "string",
                    "required": True,
                },
            },
        },
    },
}
