# allof_composition_valid

Mock server for a **Vehicle Registry API** using OpenAPI 3.1.0 `allOf` schema composition.

## Purpose

Stress-tests the plugin's handling of `allOf` schema composition. Base schemas are extended via `allOf` to add type-specific fields. All responses are correct and this server **should PASS** validation.

## Schema Features

- `components/schemas`: `Vehicle` (base), `ElectricVehicle` (allOf Vehicle), `GasVehicle` (allOf Vehicle), `NewVehicle`
- `allOf` used to compose `ElectricVehicle` and `GasVehicle` from `Vehicle`
- `$ref` within `allOf` arrays
- `enum` on `type` field (`"electric"`, `"gas"`) and `fuel_type`
- OpenAPI version `3.1.0`

## Endpoints

### GET /vehicles
Returns all vehicles. Mix of electric and gas vehicles; response items reference `Vehicle` base schema.

**Example response:**
```json
[
  { "id": 1, "make": "Tesla", "model": "Model 3", "year": 2023, "type": "electric", "battery_capacity_kwh": 82.0, "range_km": 576 },
  { "id": 2, "make": "Toyota", "model": "Camry", "year": 2022, "type": "gas", "engine_size_liters": 2.5, "fuel_type": "gasoline" }
]
```

### POST /vehicles
Registers a new vehicle. Request uses `NewVehicle` schema; response uses `ElectricVehicle` schema (with allOf).

**Example request:**
```json
{ "make": "Rivian", "model": "R1T", "year": 2024, "type": "electric", "battery_capacity_kwh": 135.0, "range_km": 515 }
```

## Expected Test Outcome

**PASS** — All responses match the composed schemas.
