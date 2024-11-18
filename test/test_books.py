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


def test_list_books(client):
    response = client.get("/api/v1/books/")
    assert response.status_code == 200
    books = response.json()
    assert len(books) > 0
    assert books[0]["title"] == book_data["title"]


def test_search_books_by_author(client):
    response = client.get("/api/v1/books/", params={"author": book_data["author"]})
    assert response.status_code == 200
    books = response.json()
    assert len(books) > 0
    assert books[0]["author"] == book_data["author"]


# Test: Buscar libros por título
def test_search_books_by_title(client):
    response = client.get("/api/v1/books/search/", params={"query": book_data["title"]})
    assert response.status_code == 200
    books = response.json()
    assert len(books) > 0
    assert books[0]["title"] == book_data["title"]


# Test: Actualizar un libro
def test_update_book(client):
    # Obtener el ID del libro
    response = client.get("/api/v1/books/")
    book_id = response.json()[0]["id"]

    # Actualizar el libro
    response = client.put(f"/api/v1/books/{book_id}/", json=updated_book_data)
    assert response.status_code == 200
    updated_book = response.json()
    assert updated_book["title"] == updated_book_data["title"]
    assert updated_book["year"] == updated_book_data["year"]


# Test: Eliminar un libro
def test_delete_book(client):
    # Obtener el ID del libro
    response = client.get("/api/v1/books/")
    book_id = response.json()[0]["id"]

    # Eliminar el libro
    response = client.delete(f"/api/v1/books/{book_id}/")
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"

    # Verificar que el libro ya no existe
    response = client.get("/api/v1/books/")
    books = response.json()
    assert len(books) == 0
