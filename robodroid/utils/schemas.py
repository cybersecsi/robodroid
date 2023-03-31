"""
  This module contains the schemas (for YAML files currently) that will be validated with 'cerberus'
"""

lib_config_schema = {
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

config_schema = {
    "id": {
        "type": "string",
        "required": True,
    },
    "host": {
        "type": "string",
        "required": True,
    },
    "port": {
        "type": "integer",
        "required": True,
    },
    "type": {
        "type": "string",
        "required": True,
    },
    "device-name": {
        "type": "string",
        "required": True,
    },
    "init": {
        "type": "dict",
        "required": False,
        "schema": {
            "packages": {
                "type": "list",
                "required": True,
            }
        },
    },
    "behaviors": {
        "type": "list",
        "required": True,
        "schema": {
            "type": "dict",
            "required": True,
            "schema": {
                "id": {"type": "string", "required": True},
                "inputs": {
                    "type": "list",
                    "required": False,
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
            },
        },
    },
}
