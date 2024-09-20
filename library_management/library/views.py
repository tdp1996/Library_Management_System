from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from .models import Book, Member
from .forms import SignUpForm, LoginForm



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
            return redirect('/login/')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def member_login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def member_profile(request, id):
    user_profile = get_object_or_404(Member, MemberID=id)
    return render(request, 'profile.html', {'user_profile': user_profile})


def logout_view(request):
    logout(request)
    return redirect('/')


def homepage(request):
    classic_books = Book.objects.filter(Genre__icontains='classic')[:5]
    children_books = Book.objects.filter(Genre__icontains='children')[:5]
    history_books = Book.objects.filter(Genre__icontains='history')[:5]
    thriller_books = Book.objects.filter(Genre__icontains='thriller')[:5]
    science_books = Book.objects.filter(Genre__icontains='science')[:5]
    context = {
        'classic_books': classic_books,
        'children_books': children_books,
        'history_books': history_books,
        'thriller_books': thriller_books,
        'science_books': science_books,
    }
    
    return render(request, 'main.html', context)
