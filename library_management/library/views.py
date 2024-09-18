from django.contrib.auth import login
from django.db.models import Q
from django.shortcuts import get_list_or_404, render, redirect
from .models import Book
from .forms import SignUpForm



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


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Đăng nhập ngay sau khi đăng ký thành công
            return redirect('/')  # Chuyển hướng đến trang chủ
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})



