from django.test import TestCase
from django.urls import reverse
from ..models import Book

class SearchBookViewTest(TestCase):
    def setUp(self):
        Book.objects.create(ISBN="111", Book_Title="Django Testing", Book_Author="John Doe", Year_Of_Publication=2021, Publisher="Test Publisher", Genre="Technology")
        Book.objects.create(ISBN="222", Book_Title="Learning Python", Book_Author="Jane Doe", Year_Of_Publication=2020, Publisher="Tech Publisher", Genre="Education")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('library:search_books'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_books.html')

    def test_search_books_no_query(self):
        response = self.client.get(reverse('library:search_books'), {'query': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No books found matching')
        self.assertEqual(response.context['results'], [])

    def test_search_books_with_query(self):
        response = self.client.get(reverse('library:search_books'), {'query': 'Django'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['results']), 1)
        self.assertEqual(response.context['results'][0].Book_Title, "Django Testing")

    def test_search_books_multiple_results(self):
        response = self.client.get(reverse('library:search_books'), {'query': 'Doe'}) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['results']), 2) 
        self.assertIn("Django Testing", [book.Book_Title for book in response.context['results']]) 
        self.assertIn("Learning Python", [book.Book_Title for book in response.context['results']]) 


class CategoryBooksViewTest(TestCase):
    def setUp(self):
        self.book1 = Book.objects.create(
            ISBN="111",
            Book_Title="Sample Book 1", 
            Book_Author="Author 1", 
            Genre="Fiction", 
            Year_Of_Publication=2020,
            Publisher="Publisher 1",
            Amount=10, Available=10
        )
        self.book2 = Book.objects.create(
            ISBN="222",
            Book_Title="Sample Book 2", 
            Book_Author="Author 2", 
            Genre="Non-Fiction", 
            Year_Of_Publication=2021,
            Publisher="Publisher 2",
            Amount=5, Available=5
        )

    def test_genre_in_context(self):
        response = self.client.get(reverse('library:category_books', args=['Fiction']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['genre'], 'Fiction')
        

    def test_category_books_with_invalid_genre(self):
        response = self.client.get(reverse('library:category_books', args=['Sci-Fi']))
        self.assertEqual(response.status_code, 404)
        