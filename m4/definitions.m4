define(<|__ADDON_DEFN__|>, <|
    "addon": {
      "type": "object",
      "properties": {
        "blocklisted": {
          "type": "boolean"
        },
        "description": {
          "type": ["string", "null"]
        },
        "name": {
          "type": "string"
        },
        "userDisabled": {
          "type": ["boolean", "integer"]
        },
        "appDisabled": {
          "type": "boolean"
        },
        "version": {
          "type": ["string", "number"]
        },
        "scope": {
          "type": "integer"
        },
        "type": {
          "type": "string"
        },
        "foreignInstall": {
          "type": [
            "integer",
            "boolean"
          ]
        },
        "hasBinaryComponents": {
          "type": "boolean"
        },
        "installDay": {
          "type": ["integer", "null"],
          "minimum": 0
        },
        "updateDay": {
          "type": "integer",
          "minimum": 0
        },
        "signedState": {
          "type": "integer"
        },
        "isSystem": {
          "type": "boolean"
        }
      }
    }
|>)

define(<|__ADAPTER_DEFN__|>, <|
  "adapter": {
      "type": "object",
      "properties": {
        "description": {
          "type": ["string", "null"]
        },
        "vendorID": {
          "type": ["string", "null"]
        },
        "deviceID": {
          "type": ["string", "null"]
        },
        "subsysID": {
          "type": ["string", "null"]
        },
        "RAM": {
          "type": ["integer", "null"]
        },
        "driver": {
          "type": ["string", "null"]
        },
        "driverVersion": {
          "type": ["string", "null"]
        },
        "driverDate": {
          "type": ["string", "null"]
        },
        "GPUActive": {
          "type": "boolean"
        }
      }
    }
|>)

define(<|__FEATURES_DEFN__|>, <|
    "features": {
      "type": "object",
      "properties": {
        "compositor": {
          "type": "string"
        },
        "d2d": {
          "type": ["object", "null"],
          "items": {
            "$ref": "#/definitions/feature"
          }
        },
        "d3d11": {
          "type": ["object", "null"],
          "items": {
            "$ref": "#/definitions/feature"
          }
        },
        "opengl": {
          "type": ["object", "null"],
          "items": {
            "$ref": "#/definitions/feature"
          }
        },
        "webgl": {
          "type": ["object", "null"],
          "items": {
            "$ref": "#/definitions/feature"
          }
        },
        "gpuProcess": {
          "type": ["object", "null"],
          "properties": {
            "status": {
              "type": ["string", "null"]
            }
          }
        }
      }
    },
    "feature": {
      "type": "object",
      "properties": {
        "status": {
          "type": ["string", "null"]
        },
        "failureId": {
          "type": ["string", "null"]
        },
        "version": {
          "type": ["string", "null"]
        },
        "warp": {
          "type": ["boolean", "null"]
        },
        "textureSharing": {
          "type": ["boolean", "null"]
        }
      }
    }
|>)

define(<|__GMPLUGIN_DEFN__|>, <|
    "gmPlugin": {
      "type": "object",
      "properties": {
        "version": {
          "type": ["string", "null"]
        },
        "userDisabled": {
          "type": "boolean"
        },
        "applyBackgroundUpdates": {
          "type": [
            "integer",
            "boolean"
          ]
        }
      }
    }
|>)

define(<|__MONITOR_DEFN__|>, <|
    "monitor": {
      "type": "object",
      "properties": {
        "screenWidth": {
          "type": "integer"
        },
        "screenHeight": {
          "type": "integer"
        },
        "refreshRate": {
          "type": "number"
        },
        "pseudoDisplay": {
          "type": "boolean"
        },
        "scale": {
          "type": "number"
        }
      }
    }
|>)

define(<|__PLUGIN_DEFN__|>, <|
    "plugin": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "version": {
          "type": "string"
        },
        "description": {
          "type": "string"
        },
        "blocklisted": {
          "type": "boolean"
        },
        "disabled": {
          "type": "boolean"
        },
        "clicktoplay": {
          "type": "boolean"
        },
        "mimeTypes": {
          "type": ["array", "object"],
          "items": {
            "type": "string"
          }
        },
        "updateDay": {
          "type": "integer"
        }
      }
    }
|>)
