import pytest


book_data = {
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "year": 1925,
    "isbn": "9780743273565"
}

updated_book_data = {
    "title": "The Great Gatsby - Updated",
    "author": "F. Scott Fitzgerald",
    "year": 1926,
    "isbn": "9780743273565"
}


def test_add_book(client):
    response = client.post("/api/v1/books/", json=book_data)
    assert response.status_code == 200
    assert response.json()["title"] == book_data["title"]


def test_list_all_books(client):
    # Crear un libro para asegurarse de que la base de datos no está vacía
    client.post("/api/v1/books/", json=book_data)

    # Recuperar todos los libros
    response = client.get("/api/v1/books/")
    assert response.status_code == 200
    books = response.json()
    assert len(books) > 0
    assert books[0]["title"] == book_data["title"]


def test_list_all_books_empty(client):
    response = client.get("/api/v1/books/")
    assert response.status_code == 200
    assert response.json() == []


def test_search_books_by_author(client):
    client.post("/api/v1/books/", json=book_data)
    response = client.get("/api/v1/book/", params={"author": book_data["author"]})
    assert response.status_code == 200
    books = response.json()
    assert len(books) > 0
    assert books[0]["author"] == book_data["author"]


def test_update_book(client):
    response = client.post("/api/v1/books/", json=book_data)
    assert response.status_code == 200
    book_id = response.json()["id"]

    response = client.put(f"/api/v1/books/{book_id}/", json=updated_book_data)
    assert response.status_code == 200
    updated_book = response.json()
    assert updated_book["title"] == updated_book_data["title"]
    assert updated_book["year"] == updated_book_data["year"]


def test_delete_book(client):
    response = client.post("/api/v1/books/", json=book_data)
    assert response.status_code == 200
    book_id = response.json()["id"]

    response = client.delete(f"/api/v1/books/{book_id}/")
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"

    response = client.get("/api/v1/books/")
    books = response.json()
    assert len(books) == 0


def test_get_book_by_id(client):
    response = client.post("/api/v1/books/", json=book_data)
    assert response.status_code == 200
    book_id = response.json()["id"]

    response = client.get(f"/api/v1/books/{book_id}/")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    book = response.json()
    assert book["id"] == book_id
    assert book["title"] == book_data["title"]


def test_add_duplicate_book(client):
    response = client.post("/api/v1/books/", json=book_data)
    assert response.status_code == 200

    response = client.post("/api/v1/books/", json=book_data)
    assert response.status_code == 400
    assert response.json()["detail"] == f"A book with ISBN {book_data['isbn']} already exists."


def test_search_books_by_any_field(client):
    client.post("/api/v1/books/", json=book_data)

    response = client.get("/api/v1/books/search/", params={"query": "Gatsby"})
    assert response.status_code == 200
    books = response.json()
    assert len(books) > 0
    assert books[0]["title"] == book_data["title"]

    response = client.get("/api/v1/books/search/", params={"query": "Fitzgerald"})
    assert response.status_code == 200
    books = response.json()
    assert len(books) > 0
    assert books[0]["author"] == book_data["author"]

    response = client.get("/api/v1/books/search/", params={"query": "1925"})
    assert response.status_code == 200
    books = response.json()
    assert len(books) > 0
    assert books[0]["year"] == book_data["year"]

    response = client.get("/api/v1/books/search/", params={"query": "9780743273565"})
    assert response.status_code == 200
    books = response.json()
    assert len(books) > 0
    assert books[0]["isbn"] == book_data["isbn"]


def test_search_books_no_results(client):
    response = client.get("/api/v1/books/search/", params={"query": "Nonexistent"})
    assert response.status_code == 404
    assert response.json()["detail"] == "No books found matching the query."
