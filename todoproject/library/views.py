from django.shortcuts import get_object_or_404, render

from .models import Book


def book_list(request):
    books = Book.objects.select_related("author", "publisher").prefetch_related("categories")
    return render(request, "library/book_list.html", {"books": books})


def book_detail(request, pk):
    book = get_object_or_404(
        Book.objects.select_related("author", "publisher", "publication")
        .prefetch_related("categories"),
        pk=pk,
    )
    return render(request, "library/book_detail.html", {"book": book})