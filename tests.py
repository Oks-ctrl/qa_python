import pytest
from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()

        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        assert len(collector.get_books_genre()) == 2
        assert collector.get_book_genre('Гордость и предубеждение и зомби') == ''
        assert collector.get_book_genre('Что делать, если ваш кот хочет вас убить') == ''


    
    @pytest.mark.parametrize("book_name,expected", [
        ("Властелин колец", True),
        ("", False),
        ("А" * 41, False),
    ])
    def test_add_new_book_with_various_name_lengths(self, book_name, expected):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert (book_name in collector.books_genre) == expected

    def test_set_book_genre_success(self):
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Фантастика")
        assert collector.books_genre["Книга"] == "Фантастика"

    def test_set_book_genre_invalid_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Неизвестный жанр")
        # Жанр не меняется, так как жанр не из списка
        assert collector.books_genre["Книга"] == ""

    def test_get_book_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Комедии")
        genre = collector.get_book_genre("Книга")
        assert genre == "Комедии"

    def test_get_books_with_specific_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга1", "Фантастика")
        collector.set_book_genre("Книга2", "Комедии")
        books = collector.get_books_with_specific_genre("Фантастика")
        assert books == ["Книга1"]

    def test_get_books_for_children_excludes_age_rated(self):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга1", "Ужасы")       # возрастной рейтинг
        collector.set_book_genre("Книга2", "Комедии")     # без рейтинга
        books_for_children = collector.get_books_for_children()
        assert "Книга2" in books_for_children
        assert "Книга1" not in books_for_children

    def test_add_book_in_favorites(self):
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        assert "Книга" in collector.favorites

    def test_add_book_in_favorites_only_once(self):
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.add_book_in_favorites("Книга")
        # Книга добавлена в избранное только один раз
        assert collector.favorites.count("Книга") == 1

    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.delete_book_from_favorites("Книга")
        assert "Книга" not in collector.favorites

    def test_get_list_of_favorites_books(self):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.add_book_in_favorites("Книга1")
        favorites = collector.get_list_of_favorites_books()
        assert favorites == ["Книга1"]
