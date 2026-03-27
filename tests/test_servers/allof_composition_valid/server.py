"""Mock server for a vehicle registry API using allOf schema composition.

Uses OpenAPI 3.1.0 with allOf to compose base Vehicle schema with
type-specific extensions (ElectricVehicle, GasVehicle). All responses
are correct and should PASS validation.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

VEHICLES_DB = [
    {
        "id": 1,
        "make": "Tesla",
        "model": "Model 3",
        "year": 2023,
        "type": "electric",
        "battery_capacity_kwh": 82.0,
        "range_km": 576,
    },
    {
        "id": 2,
        "make": "Toyota",
        "model": "Camry",
        "year": 2022,
        "type": "gas",
        "engine_size_liters": 2.5,
        "fuel_type": "gasoline",
    },
]


@app.route("/openapi.json")
def openapi():
    """Return OpenAPI 3.1.0 spec with allOf schema composition."""
    return jsonify(
        {
            "openapi": "3.1.0",
            "info": {
                "title": "Vehicle Registry API",
                "version": "1.0.0",
                "description": "API for managing vehicle registrations using allOf composition",
            },
            "components": {
                "schemas": {
                    "Vehicle": {
                        "type": "object",
                        "description": "Base vehicle schema",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "description": "Unique vehicle identifier",
                            },
                            "make": {
                                "type": "string",
                                "description": "Vehicle manufacturer",
                            },
                            "model": {
                                "type": "string",
                                "description": "Vehicle model name",
                            },
                            "year": {
                                "type": "integer",
                                "description": "Model year",
                            },
                            "type": {
                                "type": "string",
                                "description": "Propulsion type",
                                "enum": ["electric", "gas"],
                            },
                        },
                    },
                    "ElectricVehicle": {
                        "description": "An electric vehicle extending the base Vehicle schema",
                        "allOf": [
                            {"$ref": "#/components/schemas/Vehicle"},
                            {
                                "type": "object",
                                "properties": {
                                    "battery_capacity_kwh": {
                                        "type": "number",
                                        "description": "Battery capacity in kilowatt-hours",
                                    },
                                    "range_km": {
                                        "type": "integer",
                                        "description": "Estimated range in kilometers",
                                    },
                                },
                            },
                        ],
                    },
                    "GasVehicle": {
                        "description": "A gasoline/diesel vehicle extending the base Vehicle schema",
                        "allOf": [
                            {"$ref": "#/components/schemas/Vehicle"},
                            {
                                "type": "object",
                                "properties": {
                                    "engine_size_liters": {
                                        "type": "number",
                                        "description": "Engine displacement in liters",
                                    },
                                    "fuel_type": {
                                        "type": "string",
                                        "enum": ["gasoline", "diesel"],
                                        "description": "Type of fuel",
                                    },
                                },
                            },
                        ],
                    },
                    "NewVehicle": {
                        "description": "Payload for registering a new vehicle",
                        "allOf": [
                            {
                                "type": "object",
                                "properties": {
                                    "make": {
                                        "type": "string",
                                        "description": "Vehicle manufacturer",
                                    },
                                    "model": {
                                        "type": "string",
                                        "description": "Vehicle model name",
                                    },
                                    "year": {
                                        "type": "integer",
                                        "description": "Model year",
                                    },
                                    "type": {
                                        "type": "string",
                                        "enum": ["electric", "gas"],
                                        "description": "Propulsion type",
                                    },
                                    "battery_capacity_kwh": {
                                        "type": "number",
                                        "description": "Battery capacity (electric only)",
                                    },
                                    "range_km": {
                                        "type": "integer",
                                        "description": "Range in km (electric only)",
                                    },
                                    "engine_size_liters": {
                                        "type": "number",
                                        "description": "Engine size in liters (gas only)",
                                    },
                                    "fuel_type": {
                                        "type": "string",
                                        "enum": ["gasoline", "diesel"],
                                        "description": "Fuel type (gas only)",
                                    },
                                },
                            }
                        ],
                    },
                }
            },
            "paths": {
                "/vehicles": {
                    "get": {
                        "summary": "List all registered vehicles",
                        "description": "Returns all vehicles in the registry",
                        "responses": {
                            "200": {
                                "description": "List of vehicles",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "array",
                                            "description": "Array of vehicles",
                                            "items": {
                                                "$ref": "#/components/schemas/Vehicle"
                                            },
                                        },
                                        "example": [
                                            {
                                                "id": 1,
                                                "make": "Tesla",
                                                "model": "Model 3",
                                                "year": 2023,
                                                "type": "electric",
                                                "battery_capacity_kwh": 82.0,
                                                "range_km": 576,
                                            },
                                            {
                                                "id": 2,
                                                "make": "Toyota",
                                                "model": "Camry",
                                                "year": 2022,
                                                "type": "gas",
                                                "engine_size_liters": 2.5,
                                                "fuel_type": "gasoline",
                                            },
                                        ],
                                    }
                                },
                            }
                        },
                    },
                    "post": {
                        "summary": "Register a new vehicle",
                        "description": "Adds a vehicle to the registry",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/NewVehicle"
                                    },
                                    "example": {
                                        "make": "Rivian",
                                        "model": "R1T",
                                        "year": 2024,
                                        "type": "electric",
                                        "battery_capacity_kwh": 135.0,
                                        "range_km": 515,
                                    },
                                }
                            },
                        },
                        "responses": {
                            "201": {
                                "description": "Vehicle registered",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/ElectricVehicle"
                                        },
                                        "example": {
                                            "id": 3,
                                            "make": "Rivian",
                                            "model": "R1T",
                                            "year": 2024,
                                            "type": "electric",
                                            "battery_capacity_kwh": 135.0,
                                            "range_km": 515,
                                        },
                                    }
                                },
                            }
                        },
                    },
                }
            },
        }
    )


@app.route("/vehicles", methods=["GET"])
def list_vehicles():
    """Return all registered vehicles."""
    return jsonify(VEHICLES_DB)


@app.route("/vehicles", methods=["POST"])
def register_vehicle():
    """Register a new vehicle."""
    data = request.get_json()
    vehicle_type = data.get("type")
    if vehicle_type not in ("electric", "gas"):
        return jsonify({"error": f"Invalid type '{vehicle_type}'. Must be 'electric' or 'gas'."}), 400
    fuel_type = data.get("fuel_type")
    if fuel_type is not None and fuel_type not in ("gasoline", "diesel"):
        return jsonify({"error": f"Invalid fuel_type '{fuel_type}'. Must be 'gasoline' or 'diesel'."}), 400
    new_vehicle = {
        "id": len(VEHICLES_DB) + 1,
        "make": data["make"],
        "model": data["model"],
        "year": data["year"],
        "type": vehicle_type,
    }
    if vehicle_type == "electric":
        new_vehicle["battery_capacity_kwh"] = data.get("battery_capacity_kwh", 75.0)
        new_vehicle["range_km"] = data.get("range_km", 400)
    else:
        new_vehicle["engine_size_liters"] = data.get("engine_size_liters", 2.0)
        new_vehicle["fuel_type"] = fuel_type or "gasoline"
    return jsonify(new_vehicle), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
