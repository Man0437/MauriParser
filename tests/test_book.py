import pytest

from mauri.models.books import Books, BookRepository

def test_book():
    books = Books(1, "name", "type", "author", 19.20, "EURO")
    assert books.id == 1
    assert books.name == "name"
    assert books.type == "type"
    assert books.author == "author"
    assert books.price == 19.20
    assert books.money == "EURO"
    