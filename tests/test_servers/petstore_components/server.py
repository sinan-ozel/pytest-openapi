"""Mock server implementing a simplified Petstore API.

Based on the classic OpenAPI Petstore example (https://petstore3.swagger.io),
adapted for OpenAPI 3.1.0 with components/schemas. All responses are correct
and should PASS validation.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

PETS_DB = {
    1: {"id": 1, "name": "Fluffy", "status": "available", "tag": "cat"},
    2: {"id": 2, "name": "Rex", "status": "adopted", "tag": "dog"},
}
next_id = 3


@app.route("/openapi.json")
def openapi():
    """Return OpenAPI 3.1.0 Petstore spec with components/schemas."""
    return jsonify(
        {
            "openapi": "3.1.0",
            "info": {
                "title": "Petstore API",
                "version": "1.0.0",
                "description": "A sample Petstore API based on the OpenAPI 3.1.0 Petstore spec",
            },
            "components": {
                "schemas": {
                    "Pet": {
                        "type": "object",
                        "description": "A pet available in the store",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "format": "int64",
                                "description": "Unique identifier for the pet",
                            },
                            "name": {
                                "type": "string",
                                "description": "Name of the pet",
                            },
                            "status": {
                                "type": "string",
                                "description": "Adoption status of the pet",
                                "enum": ["available", "pending", "adopted"],
                            },
                            "tag": {
                                "type": "string",
                                "description": "Optional tag or category label",
                            },
                        },
                    },
                    "NewPet": {
                        "type": "object",
                        "description": "Payload for adding a new pet",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name of the new pet",
                            },
                            "status": {
                                "type": "string",
                                "description": "Initial adoption status",
                                "enum": ["available", "pending", "adopted"],
                            },
                            "tag": {
                                "type": "string",
                                "description": "Optional tag or category label",
                            },
                        },
                    },
                    "Error": {
                        "type": "object",
                        "description": "Error response body",
                        "properties": {
                            "code": {
                                "type": "integer",
                                "format": "int32",
                                "description": "HTTP-style error code",
                            },
                            "message": {
                                "type": "string",
                                "description": "Human-readable error message",
                            },
                        },
                    },
                }
            },
            "paths": {
                "/pets": {
                    "get": {
                        "summary": "List all pets",
                        "description": "Returns a list of all pets in the store",
                        "responses": {
                            "200": {
                                "description": "A list of pets",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "array",
                                            "description": "Array of pet objects",
                                            "items": {
                                                "$ref": "#/components/schemas/Pet"
                                            },
                                        },
                                        "example": [
                                            {
                                                "id": 1,
                                                "name": "Fluffy",
                                                "status": "available",
                                                "tag": "cat",
                                            },
                                            {
                                                "id": 2,
                                                "name": "Rex",
                                                "status": "adopted",
                                                "tag": "dog",
                                            },
                                        ],
                                    }
                                },
                            }
                        },
                    },
                    "post": {
                        "summary": "Add a new pet",
                        "description": "Creates a new pet entry in the store",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/NewPet"
                                    },
                                    "example": {
                                        "name": "Whiskers",
                                        "status": "available",
                                        "tag": "cat",
                                    },
                                }
                            },
                        },
                        "responses": {
                            "201": {
                                "description": "Pet created successfully",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Pet"
                                        },
                                        "example": {
                                            "id": 3,
                                            "name": "Whiskers",
                                            "status": "available",
                                            "tag": "cat",
                                        },
                                    }
                                },
                            }
                        },
                    },
                },
                "/pets/{petId}": {
                    "get": {
                        "summary": "Get a pet by ID",
                        "description": "Returns a single pet by its ID",
                        "parameters": [
                            {
                                "name": "petId",
                                "in": "path",
                                "required": True,
                                "description": "ID of the pet to retrieve",
                                "schema": {
                                    "type": "integer",
                                    "format": "int64",
                                },
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "A single pet",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Pet"
                                        },
                                        "example": {
                                            "id": 1,
                                            "name": "Fluffy",
                                            "status": "available",
                                            "tag": "cat",
                                        },
                                    }
                                },
                            },
                            "404": {
                                "description": "Pet not found",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Error"
                                        },
                                        "example": {
                                            "code": 404,
                                            "message": "Pet not found",
                                        },
                                    }
                                },
                            },
                        },
                    },
                    "delete": {
                        "summary": "Delete a pet",
                        "description": "Removes a pet from the store",
                        "parameters": [
                            {
                                "name": "petId",
                                "in": "path",
                                "required": True,
                                "description": "ID of the pet to delete",
                                "schema": {
                                    "type": "integer",
                                    "format": "int64",
                                },
                            }
                        ],
                        "responses": {
                            "204": {
                                "description": "Pet deleted successfully",
                            },
                            "404": {
                                "description": "Pet not found",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Error"
                                        },
                                        "example": {
                                            "code": 404,
                                            "message": "Pet not found",
                                        },
                                    }
                                },
                            },
                        },
                    },
                },
            },
        }
    )


@app.route("/pets", methods=["GET"])
def list_pets():
    """List all pets."""
    return jsonify(list(PETS_DB.values()))


@app.route("/pets", methods=["POST"])
def create_pet():
    """Create a new pet."""
    global next_id
    data = request.get_json()
    pet = {
        "id": next_id,
        "name": data["name"],
        "status": data.get("status", "available"),
        "tag": data.get("tag", ""),
    }
    PETS_DB[next_id] = pet
    next_id += 1
    return jsonify(pet), 201


@app.route("/pets/<int:pet_id>", methods=["GET"])
def get_pet(pet_id):
    """Get a pet by ID."""
    if pet_id not in PETS_DB:
        return jsonify({"code": 404, "message": "Pet not found"}), 404
    return jsonify(PETS_DB[pet_id])


@app.route("/pets/<int:pet_id>", methods=["DELETE"])
def delete_pet(pet_id):
    """Delete a pet by ID."""
    if pet_id not in PETS_DB:
        return jsonify({"code": 404, "message": "Pet not found"}), 404
    del PETS_DB[pet_id]
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
