from django.shortcuts import render, get_list_or_404
from .models import Book
# from .forms import BookSearchForm

from django.db.models import Q


def main(request):
    return render(request, 'main.html')


def search_books(request):
    query = request.GET.get('query', '')
    results = []
    
    if query:
        results = Book.objects.filter(
            Q(Book_Title__icontains=query) |
            Q(Book_Author__icontains=query) |
            Q(Genre__icontains=query) |
            Q(Publisher__icontains=query)
        )

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'search_books.html', context)


def category_books(request, genre):
    books = get_list_or_404(Book, Genre__icontains=genre)
    return render(request, 'category_books.html', {'books': books, 'genre': genre})


def details(request, id):
    books = Book.objects.get(BookID=id)
    context = {
        'books': books,
    }
    return render(request, 'details.html', context)



