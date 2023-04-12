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
            "package_name": {
                "type": "string",
                "required": True,
            },
            "description": {
                "type": "string",
                "required": True,
            },
            "permissions": {
                "type": "list",
                "required": False,
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
    "outputs": {
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
    "device_name": {
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
    "workflow": {
        "type": "list",
        "required": True,
        "schema": {
            "type": "dict",
            "required": True,
            "schema": {
                "id": {"type": "string", "required": True},
                "name": {"type": "string", "required": True},
                "type": {"type": "string", "required": True},
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
                                "required": True,
                            },
                        },
                    },
                },
            },
        },
    },
}
