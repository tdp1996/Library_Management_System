from django.test import TestCase
from django.urls import reverse
from ..models import Book, Member

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
            Genre="Horror", 
            Year_Of_Publication=2021,
            Publisher="Publisher 2",
            Amount=5, Available=5
        )

    def test_genre_in_context(self):
        response = self.client.get(reverse('library:category_books', args=['Fiction']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['genre'], 'Fiction')

    def test_category_books_with_valid_genre(self):
        response = self.client.get(reverse('library:category_books', args=['Fiction']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['books']), 1)
        
    def test_category_books_with_invalid_genre(self):
        response = self.client.get(reverse('library:category_books', args=['Sci-Fi']))
        self.assertEqual(response.status_code, 404)
        
class DetailsViewTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            ISBN="111",
            Book_Title="Sample Book", 
            Book_Author="Author 1", 
            Genre="Fiction", 
            Year_Of_Publication=2020,
            Publisher="Publisher 1",
            Amount=10, Available=10
        )

    def test_book_details_valid_id(self):
        response = self.client.get(reverse('library:details', args=[self.book.BookID]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'details.html')
        self.assertEqual(response.context['books'].Book_Title, "Sample Book")

    def test_book_details_invalid_id(self):
        response = self.client.get(reverse('library:details', args=['150']))
        self.assertEqual(response.status_code, 404)


class HomepageViewTest(TestCase):
    def setUp(self):
        genres = ['Classic', 'Children', 'History', 'Thriller', 'Science']
        for i, genre in enumerate(genres):
            for j in range(10):
                Book.objects.create(
                    ISBN=f"1234567890-{i}-{j}",
                    Book_Title=f"Sample Book {i}-{j}",
                    Book_Author=f"Author {i}",
                    Year_Of_Publication=2020,
                    Publisher="Sample Publisher",
                    Genre=genre,
                    Amount=10,
                    Available=5,
                )
    
    def test_homepage_status_code(self):
        response = self.client.get(reverse('library:homepage'))  
        self.assertEqual(response.status_code, 200)
    
    def test_homepage_template_used(self):
        response = self.client.get(reverse('library:homepage'))
        self.assertTemplateUsed(response, 'main.html')

    def test_homepage_context_data(self):
        response = self.client.get(reverse('library:homepage'))
        self.assertEqual(len(response.context['classic_books']), 5)
        self.assertEqual(len(response.context['children_books']), 5)
        self.assertEqual(len(response.context['history_books']), 5)
        self.assertEqual(len(response.context['thriller_books']), 5)
        self.assertEqual(len(response.context['science_books']), 5)
        classic_books = response.context['classic_books']
        self.assertEqual(classic_books[0].Book_Title, 'Sample Book 0-0')

    def test_homepage_limited_books_per_category(self):
        response = self.client.get(reverse('library:homepage'))
        
        self.assertTrue(all(len(response.context[category]) <= 5 for category in [
            'classic_books', 'children_books', 'history_books', 'thriller_books', 'science_books'
        ]))

class MemberProfileTest(TestCase):
    def setUp(self):
        self.member = Member.objects.create_user(
            Email="testuser@example.com",
            Name="Test User",
            Phone="0123456789",
            Address="123 Street"
        )
    
    def test_member_profile_status_code(self):
        response = self.client.get(reverse('library:member_profile', args=[self.member.MemberID]))
        self.assertEqual(response.status_code, 200)


    def test_member_profile_template_used(self):
        response = self.client.get(reverse('library:member_profile', args=[self.member.MemberID]))
        self.assertTemplateUsed(response, 'profile.html')

    def test_member_profile_context_data(self):
        response = self.client.get(reverse('library:member_profile', args=[self.member.MemberID]))
        user_profile = response.context['user_profile']
        
        self.assertEqual(user_profile.Name, "Test User")
        self.assertEqual(user_profile.Email, "testuser@example.com")


class RegisterViewTest(TestCase):
    def test_register_page_status_code(self):
        response = self.client.get(reverse('library:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_form_in_template(self):
        response = self.client.get(reverse('library:register'))
        self.assertContains(response, '<form')

    def test_register_valid_data(self):
        test_data = {
            'Name': 'Test User',
            'Email': 'testuser@example.com',
            'Phone': '123456789',
            'Address': '123 Sample Street',
            'password1': 'testuser123',
            'password2': 'testuser123'
        }
        response = self.client.post(reverse('library:register'), data=test_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')
        self.assertTrue(Member.objects.filter(Email='testuser@example.com').exists())

    def test_register_invalid_data(self):
        form_data = {
            'Name': '', 
            'Email': 'johndoe@example.com',
        }
        response = self.client.post(reverse('library:register'), data=form_data)       
        self.assertEqual(response.status_code, 200)


class LoginViewTest(TestCase):
    def setUp(self):
        self.member = Member.objects.create_user(
            Email="testuser@example.com",
            Name="Test User",
            Phone="0123456789",
            Address="123 Street",
            password="testpassword123"
        )
    
    def test_login_view_get(self):
        response = self.client.get(reverse('library:member_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'form')

    def test_login_view_post_valid(self):
        response = self.client.post(reverse('library:member_login'),
                                    {'username': 'testuser@example.com',
                                    'password': 'testpassword123'
                                    })
        self.assertRedirects(response, '/')

    def test_login_view_post_invalid(self):

        response = self.client.post(reverse('library:member_login'), {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'form') 
        self.assertFalse(response.context['form'].is_valid())
