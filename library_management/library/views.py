from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.utils import timezone
from .forms import MemberCreationForm, LoginForm, BorrowForm
from .models import Book, Member





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
    books = get_object_or_404(Book, BookID=id)
    context = {
        'books': books,
    }
    return render(request, 'details.html', context)


def register(request):
    if request.method == 'POST':
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/login/')
    else:
        form = MemberCreationForm()
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


@login_required(login_url="/login/")
def borrow_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.BookID = book
            loan.MemberID = request.user 
            loan.LoanDate = timezone.now()
            loan.save()
            return redirect('/')  # redirect to a confirmation page or back to the book list
    else:
        form = BorrowForm()
    return render(request, 'borrow_form.html', {'form': form, 'book': book})
