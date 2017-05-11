define(<|__ENVIRONMENT__|>, <|{
    "properties": {
        "addons": {
            "properties": {
                "activeAddons": {
                    "additionalProperties": {
                        "$ref": "#/definitions/addon"
                    },
                    "type": "object"
                },
                "activeExperiment": {
                    "properties": {
                        "branch": {
                            "type": "string"
                        },
                        "id": {
                            "type": "string"
                        }
                    },
                    "type": "object"
                },
                "activeGMPlugins": {
                    "additionalProperties": {
                        "$ref": "#/definitions/gmPlugin"
                    },
                    "type": "object"
                },
                "activePlugins": {
                    "items": {
                        "$ref": "#/definitions/plugin"
                    },
                    "type": [
                        "array",
                        "object"
                    ]
                },
                "persona": {
                    "type": [
                        "string",
                        "null"
                    ]
                },
                "theme": {
                    "properties": {
                        "appDisabled": {
                            "type": "boolean"
                        },
                        "blocklisted": {
                            "type": "boolean"
                        },
                        "description": {
                            "type": [
                                "string",
                                "null"
                            ]
                        },
                        "foreignInstall": {
                            "type": [
                                "boolean",
                                "integer"
                            ]
                        },
                        "hasBinaryComponents": {
                            "type": "boolean"
                        },
                        "id": {
                            "type": "string"
                        },
                        "installDay": {
                            "minimum": 0,
                            "type": [
                                "integer",
                                "null"
                            ]
                        },
                        "name": {
                            "type": "string"
                        },
                        "scope": {
                            "type": "integer"
                        },
                        "updateDay": {
                            "minimum": 0,
                            "type": "integer"
                        },
                        "userDisabled": {
                            "type": "boolean"
                        },
                        "version": {
                            "type": "string"
                        }
                    },
                    "type": "object"
                }
            },
            "type": "object"
        },
        "build": {
            "properties": {
                "applicationId": {
                    "type": "string"
                },
                "applicationName": {
                    "type": "string"
                },
                "architecture": {
                    "type": "string"
                },
                "architecturesInBinary": {
                    "type": "string"
                },
                "buildId": {
                    "pattern": "^[0-9]{10}",
                    "type": "string"
                },
                "hotfixVersion": {
                    "type": [
                        "string",
                        "null"
                    ]
                },
                "platformVersion": {
                    "pattern": "^[0-9]{2,3}\\.",
                    "type": "string"
                },
                "vendor": {
                    "type": "string"
                },
                "version": {
                    "pattern": "^[0-9]{2,3}\\.",
                    "type": "string"
                },
                "xpcomAbi": {
                    "type": "string"
                }
            },
            "required": [
                "applicationId",
                "applicationName",
                "architecture",
                "buildId",
                "version",
                "vendor",
                "platformVersion",
                "xpcomAbi"
            ],
            "type": "object"
        },
        "partner": {
            "properties": {
                "distributionId": {
                    "type": [
                        "string",
                        "null"
                    ]
                },
                "distributionVersion": {
                    "type": [
                        "string",
                        "null"
                    ]
                },
                "distributor": {
                    "type": [
                        "string",
                        "null"
                    ]
                },
                "distributorChannel": {
                    "type": [
                        "string",
                        "null"
                    ]
                },
                "partnerId": {
                    "type": [
                        "string",
                        "null"
                    ]
                },
                "partnerNames": {
                    "type": [
                        "array",
                        "object"
                    ]
                }
            },
            "type": "object"
        },
        "profile": {
            "properties": {
                "creationDate": {
                    "type": "number"
                },
                "resetDate": {
                    "type": "number"
                }
            },
            "type": "object"
        },
        "settings": {
            "properties": {
                "attribution": {
                    "properties": {
                        "campaign": {
                            "type": "string"
                        },
                        "content": {
                            "type": "string"
                        },
                        "medium": {
                            "type": "string"
                        },
                        "source": {
                            "type": "string"
                        }
                    },
                    "type": "object"
                },
                "blocklistEnabled": {
                    "type": "boolean"
                },
                "defaultSearchEngine": {
                    "type": "string"
                },
                "defaultSearchEngineData": {
                    "properties": {
                        "loadPath": {
                            "type": [
                                "string",
                                "null"
                            ]
                        },
                        "name": {
                            "type": "string"
                        },
                        "origin": {
                            "type": "string"
                        },
                        "submissionURL": {
                            "type": "string"
                        }
                    },
                    "type": "object"
                },
                "e10sCohort": {
                    "type": "string"
                },
                "e10sEnabled": {
                    "type": "boolean"
                },
                "isDefaultBrowser": {
                    "type": [
                        "boolean",
                        "null"
                    ]
                },
                "locale": {
                    "type": "string"
                },
                "telemetryEnabled": {
                    "type": "boolean"
                },
                "update": {
                    "properties": {
                        "autoDownload": {
                            "type": "boolean"
                        },
                        "channel": {
                            "type": "string"
                        },
                        "enabled": {
                            "type": "boolean"
                        }
                    },
                    "type": "object"
                },
                "userPrefs": {
                    "type": "object"
                }
            },
            "type": "object"
        },
        "system": {
            "properties": {
                "cpu": {
                    "properties": {
                        "cores": {
                            "maximum": 2048,
                            "minimum": 1,
                            "type": [
                                "integer",
                                "null"
                            ]
                        },
                        "count": {
                            "maximum": 1024,
                            "minimum": 1,
                            "type": "integer"
                        },
                        "extensions": {
                            "type": "array"
                        },
                        "family": {
                            "type": [
                                "integer",
                                "null"
                            ]
                        },
                        "l2cacheKB": {
                            "type": [
                                "number",
                                "null"
                            ]
                        },
                        "l3cacheKB": {
                            "type": [
                                "number",
                                "null"
                            ]
                        },
                        "model": {
                            "type": [
                                "integer",
                                "null"
                            ]
                        },
                        "speedMHz": {
                            "type": [
                                "number",
                                "null"
                            ]
                        },
                        "stepping": {
                            "type": [
                                "integer",
                                "null"
                            ]
                        },
                        "vendor": {
                            "type": [
                                "string",
                                "null"
                            ]
                        }
                    },
                    "type": "object"
                },
                "device": {
                    "hardware": {
                        "type": "string"
                    },
                    "isTablet": {
                        "type": "boolean"
                    },
                    "manufacturer": {
                        "type": "string"
                    },
                    "model": {
                        "type": "string"
                    }
                },
                "gfx": {
                    "properties": {
                        "D2DEnabled": {
                            "type": [
                                "boolean",
                                "null"
                            ]
                        },
                        "DWriteEnabled": {
                            "type": [
                                "boolean",
                                "null"
                            ]
                        },
                        "adapters": {
                            "items": {
                                "$ref": "#/definitions/adapter"
                            },
                            "type": "array"
                        },
                        "features": {
                            "items": {
                                "$ref": "#/definitions/features"
                            },
                            "type": "object"
                        },
                        "monitors": {
                            "items": {
                                "$ref": "#/definitions/monitor"
                            },
                            "type": [
                                "array",
                                "object"
                            ]
                        }
                    },
                    "type": "object"
                },
                "hdd": {
                    "properties": {
                        "binary": {
                            "properties": {
                                "model": {
                                    "type": [
                                        "string",
                                        "null"
                                    ]
                                },
                                "revision": {
                                    "type": [
                                        "string",
                                        "null"
                                    ]
                                }
                            },
                            "type": "object"
                        },
                        "profile": {
                            "properties": {
                                "model": {
                                    "type": [
                                        "string",
                                        "null"
                                    ]
                                },
                                "revision": {
                                    "type": [
                                        "string",
                                        "null"
                                    ]
                                }
                            },
                            "type": "object"
                        },
                        "system": {
                            "properties": {
                                "model": {
                                    "type": [
                                        "string",
                                        "null"
                                    ]
                                },
                                "revision": {
                                    "type": [
                                        "string",
                                        "null"
                                    ]
                                }
                            },
                            "type": "object"
                        }
                    },
                    "type": "object"
                },
                "isWow64": {
                    "type": "boolean"
                },
                "memoryMB": {
                    "type": "number"
                },
                "os": {
                    "properties": {
                        "installYear": {
                            "type": "number"
                        },
                        "kernelVersion": {
                            "type": "string"
                        },
                        "locale": {
                            "type": "string"
                        },
                        "name": {
                            "type": "string"
                        },
                        "servicePackMajor": {
                            "type": "number"
                        },
                        "servicePackMinor": {
                            "type": "number"
                        },
                        "version": {
                            "type": [
                                "string",
                                "integer"
                            ]
                        },
                        "windowsBuildNumber": {
                            "type": "number"
                        },
                        "windowsUBR": {
                            "type": [
                                "number",
                                "null"
                            ]
                        }
                    },
                    "type": "object"
                }
            },
            "type": "object"
        }
    },
    "required": [
        "build",
        "partner",
        "settings",
        "system"
    ]
}|>)
