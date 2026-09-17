from datetime import date

from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse

from .models import Author, Book, BookCategory, Category, Publication, Publisher


class LibraryRelationsTestCase(TestCase):
    """Casos de prueba de relaciones: FK, OneToOne, M2M con through y related_name."""

    @classmethod
    def setUpTestData(cls):
        cls.garcia = Author.objects.create(
            name="Gabriel García Márquez",
            email="gabriel.garcia@example.com",
            birth_date=date(1927, 3, 6),
        )
        cls.allende = Author.objects.create(
            name="Isabel Allende",
            email="isabel.allende@example.com",
            birth_date=date(1942, 8, 2),
        )
        cls.random_house = Publisher.objects.create(name="Random House", city="Lima")
        cls.planeta = Publisher.objects.create(name="Planeta", city="Madrid")
        cls.novela = Category.objects.create(name="Novela", description="Ficción extensa.")
        cls.realismo = Category.objects.create(name="Realismo mágico")

        cls.pub_cien = Publication.objects.create(
            title="Cien años de soledad", publication_date=date(1967, 5, 30),
            edition=1, number_of_pages=471,
        )
        cls.pub_ines = Publication.objects.create(
            title="Inés del alma mía", publication_date=date(2006, 5, 1),
            edition=1, number_of_pages=379,
        )

        cls.cien = Book.objects.create(
            title="Cien años de soledad",
            author=cls.garcia,
            publisher=cls.random_house,
            publication=cls.pub_cien,
            isbn="9780307474728",
            price="49.90",
        )
        cls.ines = Book.objects.create(
            title="Inés del alma mía",
            author=cls.allende,
            publisher=cls.planeta,
            publication=cls.pub_ines,
            isbn="9788401352833",
            price="39.90",
        )
        BookCategory.objects.create(book=cls.cien, category=cls.novela, is_primary=True)
        BookCategory.objects.create(book=cls.cien, category=cls.realismo, is_primary=False)
        BookCategory.objects.create(book=cls.ines, category=cls.novela, is_primary=False)

    # --- Consultas en sentido directo (forward) ---
    def test_forward_book_author_and_publisher(self):
        self.assertEqual(self.cien.author.name, "Gabriel García Márquez")
        self.assertEqual(self.cien.publisher.name, "Random House")

    def test_forward_m2m_categories(self):
        self.assertEqual(set(self.cien.categories.all()), {self.novela, self.realismo})

    def test_forward_o2o_publication(self):
        self.assertEqual(self.cien.publication.number_of_pages, 471)
        self.assertEqual(self.pub_cien.title, self.cien.publication.title)

    # --- Consultas en sentido inverso (reverse, related_name) ---
    def test_reverse_author_books(self):
        self.assertEqual(list(self.garcia.books.all()), [self.cien])

    def test_reverse_publisher_books(self):
        self.assertEqual(list(self.planeta.books.all()), [self.ines])

    def test_reverse_category_books(self):
        self.assertEqual(set(self.novela.books.all()), {self.cien, self.ines})
        self.assertEqual(set(self.realismo.books.all()), {self.cien})

    def test_reverse_publication_book(self):
        """Publication es consultable desde ambos lados: book.publication y publication.book."""
        self.assertEqual(self.pub_cien.book, self.cien)
        self.assertEqual(self.pub_cien.book.title, self.cien.title)
        self.assertEqual(self.cien.publication.book.title, self.cien.title)

    # --- Filtros ---
    def test_filter_by_author_and_categories(self):
        self.assertEqual(
            list(Book.objects.filter(author__name="Isabel Allende")), [self.ines]
        )
        self.assertEqual(
            set(Book.objects.filter(categories__name="Novela")), {self.cien, self.ines}
        )
        self.assertEqual(
            list(Book.objects.filter(publisher__city="Lima")), [self.cien]
        )

    def test_filter_reverse_related_name(self):
        self.assertEqual(
            list(Author.objects.filter(books__title="Cien años de soledad")),
            [self.garcia],
        )
        self.assertEqual(
            list(Category.objects.filter(books__isbn="9788401352833")),
            [self.novela],
        )

    # --- Through model ---
    def test_through_extra_field(self):
        self.assertTrue(BookCategory.objects.get(book=self.cien, category=self.novela).is_primary)
        self.assertFalse(BookCategory.objects.get(book=self.cien, category=self.realismo).is_primary)
        self.assertEqual(BookCategory.objects.filter(book=self.cien).count(), 2)

    def test_unique_book_category(self):
        with self.assertRaises(Exception):
            BookCategory.objects.create(book=self.cien, category=self.novela)

    # --- Eliminación CASCADE y PROTECT ---
    def test_cascade_delete_author(self):
        author_pk = self.garcia.pk
        self.garcia.delete()
        self.assertFalse(Book.objects.filter(pk=self.cien.pk).exists())
        self.assertFalse(Author.objects.filter(pk=author_pk).exists())

    def test_o2o_cascade_publication(self):
        self.pub_cien.delete()
        self.assertFalse(Book.objects.filter(pk=self.cien.pk).exists())

    def test_protect_delete_publisher(self):
        with self.assertRaises(ProtectedError):
            self.random_house.delete()
        self.assertTrue(Book.objects.filter(pk=self.cien.pk).exists())
        Book.objects.filter(publisher=self.random_house).delete()
        self.random_house.delete()
        self.assertFalse(Publisher.objects.filter(pk=self.random_house.pk).exists())

    # --- Vistas: detalle muestra autor, categorías y editorial ---
    def test_book_detail_shows_relations(self):
        url = reverse("library:book_detail", args=[self.cien.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertContains(response, "Gabriel García Márquez")
        self.assertContains(response, "Random House")
        self.assertContains(response, "Novela")
        self.assertContains(response, "Realismo mágico")

    def test_book_list_shows_books(self):
        response = self.client.get(reverse("library:book_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cien años de soledad")
        self.assertContains(response, "Inés del alma mía")