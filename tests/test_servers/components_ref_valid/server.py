"""Mock server for a bookstore API using components/schemas with $ref.

This server uses OpenAPI 3.1.0 with components/schemas and $ref references
throughout its paths. All responses are correct and should PASS validation.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

BOOKS_DB = [
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
    },
    {
        "id": 2,
        "title": "Clean Code",
        "isbn": "978-0132350884",
        "year": 2008,
        "price": 39.99,
        "author": {
            "id": 2,
            "name": "Robert C. Martin",
            "bio": "Software engineer and author known as Uncle Bob",
        },
    },
]


@app.route("/openapi.json")
def openapi():
    """Return OpenAPI 3.1.0 spec with components/schemas and $ref references."""
    return jsonify(
        {
            "openapi": "3.1.0",
            "info": {
                "title": "Bookstore API",
                "version": "1.0.0",
                "description": "A bookstore catalog API with component schemas",
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
                                            },
                                            {
                                                "id": 2,
                                                "title": "Clean Code",
                                                "isbn": "978-0132350884",
                                                "year": 2008,
                                                "price": 39.99,
                                                "author": {
                                                    "id": 2,
                                                    "name": "Robert C. Martin",
                                                    "bio": "Software engineer and author known as Uncle Bob",
                                                },
                                            },
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
    """Return the full book catalog."""
    return jsonify(BOOKS_DB)


@app.route("/catalog/books", methods=["POST"])
def create_book():
    """Create a new book."""
    data = request.get_json()
    author = next(
        (
            b["author"]
            for b in BOOKS_DB
            if b["author"]["id"] == data.get("author_id", 1)
        ),
        BOOKS_DB[0]["author"],
    )
    new_book = {
        "id": len(BOOKS_DB) + 1,
        "title": data["title"],
        "isbn": data["isbn"],
        "year": data["year"],
        "price": data["price"],
        "author": author,
    }
    return jsonify(new_book), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
