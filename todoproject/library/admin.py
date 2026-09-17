from django.contrib import admin

from .models import Author, Book, BookCategory, Category, Publication, Publisher


class BookCategoryInline(admin.TabularInline):
    model = BookCategory
    extra = 1


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "birth_date")
    search_fields = ("name", "email")


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "website")
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ("title", "publication_date", "edition", "language")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publisher", "publication", "price")
    search_fields = ("title", "author__name")
    list_filter = ("publisher", "categories")
    inlines = [BookCategoryInline]


@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ("book", "category", "is_primary")
    list_filter = ("is_primary",)