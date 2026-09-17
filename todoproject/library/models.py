from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100)
    website = models.URLField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Publication(models.Model):
    title = models.CharField(max_length=120)
    publication_date = models.DateField()
    language = models.CharField(max_length=50, default="Spanish")
    edition = models.PositiveSmallIntegerField(default=1)
    number_of_pages = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["publication_date"]

    def __str__(self):
        return f"{self.title} ({self.edition}ª ed.)"


class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="books"
    )
    publisher = models.ForeignKey(
        Publisher, on_delete=models.PROTECT, related_name="books"
    )
    publication = models.OneToOneField(
        Publication, on_delete=models.CASCADE, related_name="book"
    )
    categories = models.ManyToManyField(
        Category, through="BookCategory", related_name="books"
    )
    isbn = models.CharField(max_length=13, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    summary = models.TextField(blank=True)
    cover = models.ImageField(upload_to="covers/", blank=True, null=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class BookCategory(models.Model):
    """Through model: añade is_primary al par (book, category)."""

    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="book_categories"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="book_categories"
    )
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ["book__title", "category__name"]
        constraints = [
            models.UniqueConstraint(
                fields=["book", "category"], name="unique_book_category"
            )
        ]

    def __str__(self):
        return f"{self.book.title} -> {self.category.name}"