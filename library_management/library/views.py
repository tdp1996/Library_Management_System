from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.utils import timezone
from .forms import MemberCreationForm, LoginForm, BorrowForm
from .models import Book, Member


def main(request):
    """
    Render the main page of the library system.

    :param request: HTTP request object.
    :return: Rendered main.html template.
    """

    return render(request, 'main.html')


def search_books(request):
    """
    Search for books by title, author, genre, or publisher using a query string from the GET request.

    :param request: HTTP request object with a 'query' parameter in the GET data.
    :return: Rendered search_books.html template with the search results.
    """

    query = request.GET.get('query', '')
    results = Book.objects.filter(
        Q(Book_Title__icontains=query) |
        Q(Book_Author__icontains=query) |
        Q(Genre__icontains=query) |
        Q(Publisher__icontains=query)
    ) if query else []

    return render(request, 'search_books.html', {'query': query, 'results': results})


def category_books(request, genre):
    """
    Display a list of books filtered by genre.

    :param request: HTTP request object.
    :param genre: Genre of books to filter by.
    :return: Rendered category_books.html template with the books in the genre.
    """

    books = get_list_or_404(Book, Genre__icontains=genre)
    return render(request, 'category_books.html', {'books': books, 'genre': genre})


def details(request, id):
    """
    Display detailed information about a specific book.

    :param request: HTTP request object.
    :param id: The ID of the book to display.
    :return: Rendered details.html template with book information.
    """

    books = get_object_or_404(Book, BookID=id)
    return render(request, 'details.html', {'books': books,})


def register(request):
    """
    Handle user registration. Display the registration form and create a new user if valid data is provided.

    :param request: HTTP request object.
    :return: Redirect to login page on successful registration, or render the register.html template with the form.
    """

    if request.method == 'POST':
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/login/')
    else:
        form = MemberCreationForm()
    return render(request, 'register.html', {'form': form})


def member_login(request):
    """
    Handle user login. Authenticate the user and log them in if valid credentials are provided.

    :param request: HTTP request object.
    :return: Redirect to the homepage on successful login, or render the login.html template with the form.
    """

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
    """
    Display the profile of a specific user.

    :param request: HTTP request object.
    :param id: The ID of the member whose profile is being displayed.
    :return: Rendered profile.html template with the member's information.
    """

    user_profile = get_object_or_404(Member, MemberID=id)
    return render(request, 'profile.html', {'user_profile': user_profile})


def logout_view(request):
    """
    Log out the current user and redirect to the homepage.

    :param request: HTTP request object.
    :return: Redirect to the homepage after logging out.
    """

    logout(request)
    return redirect('/')


def homepage(request):
    """
    Display the homepage with lists of books from different genres.

    :param request: HTTP request object.
    :return: Rendered main.html template with books categorized by genre.
    """
    genres = ['classic', 'children', 'history', 'thriller', 'science']
    context = {f'{genre}_books': Book.objects.filter(Genre__icontains=genre)[:5] for genre in genres}

    return render(request, 'main.html', context)


@login_required(login_url="/login/")
def borrow_book(request, book_id):
    """
    Handle the book borrowing process. Display the borrow form and create a loan entry if valid data is provided.

    :param request: HTTP request object.
    :param book_id: The ID of the book being borrowed.
    :return: Redirect to homepage after successful borrowing, or render borrow_form.html template with the form.
    """
    
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
