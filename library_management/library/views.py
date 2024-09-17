from django.shortcuts import render, get_list_or_404
from .models import Book
# from .forms import BookSearchForm

from django.db.models import Q

# def books(request):
#     thebooks = Book.objects.order_by('?')[:5]
#     context = {
#         'thebooks': thebooks,
#     }
#     return render(request, 'all_books.html', context)

# def details(request, id):
#     thebooks = Book.objects.get(BookID=id)
#     context = {
#         'thebooks': thebooks,
#     }
#     return render(request, 'details.html', context)

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
    books = get_list_or_404(Book, Genre__icontains=genre)  # Sử dụng get_list_or_404 để trả về 404 nếu không có sách nào
    return render(request, 'category_books.html', {'books': books, 'genre': genre})


