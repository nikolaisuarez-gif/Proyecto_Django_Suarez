from datetime import date

from django.core.management.base import BaseCommand

from library.models import Author, Book, BookCategory, Category, Publication, Publisher


class Command(BaseCommand):
    help = "Seed: 2 autores, 4 libros, 3 categorías y 2 editoriales."

    def handle(self, *args, **options):
        garcia = Author.objects.get_or_create(
            name="Gabriel García Márquez",
            defaults={
                "email": "gabriel.garcia@example.com",
                "birth_date": date(1927, 3, 6),
                "biography": "Escritor colombiano, premio Nobel de Literatura 1982.",
            },
        )[0]
        allende = Author.objects.get_or_create(
            name="Isabel Allende",
            defaults={
                "email": "isabel.allende@example.com",
                "birth_date": date(1942, 8, 2),
                "biography": "Escritora chilena, autora de novelas y memorias.",
            },
        )[0]

        novela, _ = Category.objects.get_or_create(name="Novela", defaults={"description": "Narrativa extensa de ficción."})
        realismo, _ = Category.objects.get_or_create(name="Realismo mágico", defaults={"description": "Elementos mágicos en un entorno realista."})
        historica, _ = Category.objects.get_or_create(name="Ficción histórica", defaults={"description": "Trama ficticia ambientada en el pasado."})

        random_house, _ = Publisher.objects.get_or_create(name="Random House", defaults={"city": "Lima", "website": "https://randomhouse.example.com"})
        planeta, _ = Publisher.objects.get_or_create(name="Planeta", defaults={"city": "Madrid", "website": "https://planeta.example.com"})

        books = [
            {
                "title": "Cien años de soledad",
                "author": garcia,
                "publisher": random_house,
                "publication_date": date(1967, 5, 30),
                "edition": 1,
                "pages": 471,
                "language": "Español",
                "isbn": "9780307474728",
                "price": "49.90",
                "summary": "La saga de la familia Buendía en el pueblo de Macondo.",
                "categories": [novela, realismo],
                "primary": realismo,
            },
            {
                "title": "El amor en los tiempos del cólera",
                "author": garcia,
                "publisher": random_house,
                "publication_date": date(1985, 12, 5),
                "edition": 1,
                "pages": 368,
                "language": "Español",
                "isbn": "9780307387264",
                "price": "45.00",
                "summary": "Historia de amor de Florentino Ariza y Fermina Daza.",
                "categories": [novela],
                "primary": novela,
            },
            {
                "title": "La casa de los espíritus",
                "author": allende,
                "publisher": planeta,
                "publication_date": date(1982, 1, 1),
                "edition": 1,
                "pages": 480,
                "language": "Español",
                "isbn": "9780525433477",
                "price": "42.50",
                "summary": "La familia Trueba a lo largo de varias generaciones.",
                "categories": [novela, realismo],
                "primary": realismo,
            },
            {
                "title": "Inés del alma mía",
                "author": allende,
                "publisher": planeta,
                "publication_date": date(2006, 5, 1),
                "edition": 1,
                "pages": 379,
                "language": "Español",
                "isbn": "9788401352833",
                "price": "39.90",
                "summary": "Vida de Inés de Suárez, conquistadora de Chile.",
                "categories": [historica],
                "primary": historica,
            },
        ]

        for data in books:
            publication, _ = Publication.objects.get_or_create(
                title=data["title"],
                defaults={
                    "publication_date": data["publication_date"],
                    "edition": data["edition"],
                    "number_of_pages": data["pages"],
                    "language": data["language"],
                },
            )
            book = Book.objects.get_or_create(
                isbn=data["isbn"],
                defaults={
                    "title": data["title"],
                    "author": data["author"],
                    "publisher": data["publisher"],
                    "publication": publication,
                    "price": data["price"],
                    "summary": data["summary"],
                },
            )[0]
            for category in data["categories"]:
                BookCategory.objects.get_or_create(
                    book=book,
                    category=category,
                    defaults={"is_primary": category == data["primary"]},
                )

        self.stdout.write(self.style.SUCCESS(
            f"Autor(es): {Author.objects.count()} | Editorial(es): {Publisher.objects.count()} "
            f"| Categoría(s): {Category.objects.count()} | Libro(s): {Book.objects.count()} "
            f"| Publicación(es): {Publication.objects.count()} | Relaciones libro-categoría: {BookCategory.objects.count()}"
        ))