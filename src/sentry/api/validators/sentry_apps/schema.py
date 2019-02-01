from __future__ import absolute_import

from jsonschema import validate as json_schema_validate

SCHEMA = {
    'type': 'object',

    'definitions': {

        # Property Types

        'uri': {
            'type': 'string',
            'format': 'uri',
        },

        'options': {
            'type': 'array',
            'items': {
                'type': 'array',
                'minItems': 2,
                'maxItems': 2,
                'items': [
                    {'type': 'string'},
                    {'anyOf': [
                        {'type': 'string'},
                        {'type': 'number'},
                    ]}
                ]
            }
        },

        'fieldset': {
            'type': 'array',
            'minItems': 1,
            'items': [
                {
                    'anyOf': [
                        {'$ref': '#/definitions/select'},
                        {'$ref': '#/definitions/text'},
                    ],
                },
            ],
        },

        # Composable Components

        'select': {
            'type': 'object',
            'properties': {
                'type': {
                    'type': 'string',
                    'enum': ['select'],
                },
                'label': {
                    'type': 'string',
                },
                'name': {
                    'type': 'string',
                },
                'uri': {
                    '$ref': '#/definitions/uri',
                },
                'options': {
                    '$ref': '#/definitions/options',
                },
            },
            'required': ['type', 'name', 'label'],
            'oneOf': [
                {'required': ['uri']},
                {'required': ['options']},
            ],
        },

        'text': {
            'type': 'object',
            'properties': {
                'type': {
                    'type': 'string',
                    'enum': ['text'],
                },
                'label': {
                    'type': 'string',
                },
                'name': {
                    'type': 'string',
                },
            },
            'required': ['type', 'label', 'name'],
        },

        'header': {
            'type': 'object',
            'properties': {
                'type': {
                    'type': 'string',
                    'enum': ['header'],
                },
                'text': {
                    'type': 'string',
                },
            },
            'required': ['type', 'text'],
        },

        'image': {
            'type': 'object',
            'properties': {
                'type': {
                    'type': 'string',
                    'enum': ['image'],
                },
                'url': {
                    'type': 'string',
                    'format': 'uri',
                    'pattern': '^https?://',
                },
                'alt': {
                    'type': 'string',
                },
            },
            'required': ['type', 'url'],
        },

        'video': {
            'type': 'object',
            'properties': {
                'type': {
                    'type': 'string',
                    'enum': ['video'],
                },
                'url': {
                    'type': 'string',
                    'format': 'uri',
                    'pattern': '^https?://',
                },
            },
            'required': ['type', 'url'],
        },

        'markdown': {
            'type': 'object',
            'properties': {
                'type': {
                    'type': 'string',
                    'enum': ['markdown'],
                },
                'text': {
                    'type': 'string',
                },
            },
            'required': ['type', 'text'],
        },

        # Feature Components

        'issue-link': {
            'type': 'object',
            'properties': {
                'type': {
                    'type': 'string',
                    'enum': ['issue-link'],
                },

                'link': {
                    'type': 'object',
                    'properties': {
                        'uri': {
                            '$ref': '#/definitions/uri',
                        },
                        'required_fields': {
                            '$ref': '#/definitions/fieldset',
                        },
                        'optional_fields': {
                            '$ref': '#/definitions/fieldset',
                        },
                    },
                    'required': ['uri', 'required_fields'],
                },

                'create': {
                    'type': 'object',
                    'properties': {
                        'uri': {
                            '$ref': '#/definitions/uri',
                        },
                        'required_fields': {
                            '$ref': '#/definitions/fieldset',
                        },
                        'optional_fields': {
                            '$ref': '#/definitions/fieldset',
                        },
                    },
                    'required': ['uri', 'required_fields'],
                },
            },
            'required': ['link', 'create'],
        },

        'alert-rule-action': {
            'type': 'object',
            'properties': {
                'type': {
                    'type': 'string',
                    'enum': ['alert-rule-action'],
                },
                'required_fields': {
                    '$ref': '#/definitions/fieldset',
                },
                'optional_fields': {
                    '$ref': '#/definitions/fieldset',
                },
            },
            'required': ['type', 'required_fields'],
        },

        'issue-media': {
            'type': 'object',
            'properties': {
                'type': {
                    'type': 'string',
                    'enum': ['issue-media'],
                },
                'title': {
                    'type': 'string',
                },
                'elements': {
                    'type': 'array',
                    'minItems': 1,
                    'items': {
                        'anyOf': [
                            {'$ref': '#/definitions/header'},
                            {'$ref': '#/definitions/markdown'},
                            {'$ref': '#/definitions/image'},
                            {'$ref': '#/definitions/video'},
                        ],
                    },
                },
            },
            'required': ['type', 'title', 'elements'],
        },
    },

    'properties': {
        'elements': {
            'type': 'array',
            'minItems': 1,
            'items': {
                'anyOf': [
                    {'$ref': '#/definitions/issue-link'},
                    {'$ref': '#/definitions/alert-rule-action'},
                    {'$ref': '#/definitions/issue-media'},
                ],
            },
        },
    },
}


def validate(instance, schema=SCHEMA):
    json_schema_validate(instance=instance, schema=schema)
