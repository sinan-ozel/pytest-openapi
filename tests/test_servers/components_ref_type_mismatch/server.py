"""Mock server exposing a type mismatch in a schema that uses $ref components.

Uses the same OpenAPI spec as components_ref_valid (bookstore), but the server
returns `year` as a string instead of an integer. This should FAIL validation.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    """Return OpenAPI 3.1.0 spec with components/schemas and $ref references."""
    return jsonify(
        {
            "openapi": "3.1.0",
            "info": {
                "title": "Bookstore API (Buggy)",
                "version": "1.0.0",
                "description": "Bookstore API where year is returned as string instead of integer",
            },
            "components": {
                "schemas": {
                    "Author": {
                        "type": "object",
                        "description": "An author of a book",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "description": "Unique author identifier",
                            },
                            "name": {
                                "type": "string",
                                "description": "Full name of the author",
                            },
                            "bio": {
                                "type": "string",
                                "description": "Short biography of the author",
                            },
                        },
                    },
                    "Book": {
                        "type": "object",
                        "description": "A book in the catalog",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "description": "Unique book identifier",
                            },
                            "title": {
                                "type": "string",
                                "description": "Title of the book",
                            },
                            "isbn": {
                                "type": "string",
                                "description": "ISBN of the book",
                            },
                            "year": {
                                "type": "integer",
                                "description": "Publication year",
                            },
                            "price": {
                                "type": "number",
                                "description": "Price in USD",
                            },
                            "author": {
                                "$ref": "#/components/schemas/Author",
                            },
                        },
                    },
                    "NewBook": {
                        "type": "object",
                        "description": "Payload for creating a new book",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Title of the book",
                            },
                            "isbn": {
                                "type": "string",
                                "description": "ISBN of the book",
                            },
                            "year": {
                                "type": "integer",
                                "description": "Publication year",
                            },
                            "price": {
                                "type": "number",
                                "description": "Price in USD",
                            },
                            "author_id": {
                                "type": "integer",
                                "description": "ID of the existing author",
                            },
                        },
                    },
                }
            },
            "paths": {
                "/catalog/books": {
                    "get": {
                        "summary": "List all books",
                        "description": "Returns the full catalog of books",
                        "responses": {
                            "200": {
                                "description": "A list of books",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "array",
                                            "description": "List of books",
                                            "items": {
                                                "$ref": "#/components/schemas/Book"
                                            },
                                        },
                                        "example": [
                                            {
                                                "id": 1,
                                                "title": "The Pragmatic Programmer",
                                                "isbn": "978-0135957059",
                                                "year": 2019,
                                                "price": 49.99,
                                                "author": {
                                                    "id": 1,
                                                    "name": "David Thomas",
                                                    "bio": "Co-author of The Pragmatic Programmer",
                                                },
                                            }
                                        ],
                                    }
                                },
                            }
                        },
                    },
                    "post": {
                        "summary": "Add a new book",
                        "description": "Adds a book to the catalog",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/NewBook"
                                    },
                                    "example": {
                                        "title": "Design Patterns",
                                        "isbn": "978-0201633610",
                                        "year": 1994,
                                        "price": 54.99,
                                        "author_id": 1,
                                    },
                                }
                            },
                        },
                        "responses": {
                            "201": {
                                "description": "Book created",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Book"
                                        },
                                        "example": {
                                            "id": 3,
                                            "title": "Design Patterns",
                                            "isbn": "978-0201633610",
                                            "year": 1994,
                                            "price": 54.99,
                                            "author": {
                                                "id": 1,
                                                "name": "David Thomas",
                                                "bio": "Co-author of The Pragmatic Programmer",
                                            },
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


@app.route("/catalog/books", methods=["GET"])
def list_books():
    """Return books with year as string (BUG: should be integer)."""
    return jsonify(
        [
            {
                "id": 1,
                "title": "The Pragmatic Programmer",
                "isbn": "978-0135957059",
                "year": "2019",  # BUG: string instead of integer
                "price": 49.99,
                "author": {
                    "id": 1,
                    "name": "David Thomas",
                    "bio": "Co-author of The Pragmatic Programmer",
                },
            }
        ]
    )


@app.route("/catalog/books", methods=["POST"])
def create_book():
    """Create a book with year as string (BUG: should be integer)."""
    data = request.get_json()
    return (
        jsonify(
            {
                "id": 3,
                "title": data.get("title", "Design Patterns"),
                "isbn": data.get("isbn", "978-0201633610"),
                "year": str(data.get("year", 1994)),  # BUG: string instead of integer
                "price": data.get("price", 54.99),
                "author": {
                    "id": 1,
                    "name": "David Thomas",
                    "bio": "Co-author of The Pragmatic Programmer",
                },
            }
        ),
        201,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
