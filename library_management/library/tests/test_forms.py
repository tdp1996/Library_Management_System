from django.test import TestCase
from django.utils import timezone
from ..forms import BorrowForm, LoginForm, MemberCreationForm
from ..models import Member

class MemberCreationFormTest(TestCase):
    def test_form_valid_data(self):
        form = MemberCreationForm(data={
            'Name': 'Test User',
            'Email': 'testuser@example.com',
            'Phone': '123456789',
            'Address': '123 Sample Street',
            'password1': 'testuser123',
            'password2': 'testuser123'
        })
        self.assertTrue(form.is_valid())
    
    def test_password_not_match(self):
        form = MemberCreationForm(data={
            'Name': 'Test User',
            'Email': 'testuser@example.com',
            'Phone': '123456789',
            'Address': '123 Sample Street',
            'password1': 'testuser123',
            'password2': 'wrongpassword'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)


class LoginFormTest(TestCase):
    def setUp(self):
        self.member = Member.objects.create_user(
            Email="testuser@example.com",
            Name="Test User",
            Phone="0123456789",
            Address="123 Street",
            password="testpassword123"
        )
    def test_form_valid_data(self):
        form = LoginForm(data={'username' : 'testuser@example.com',
                               'password' : 'testpassword123'})
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        form = LoginForm(data={'username': 'user123', 'password': 'testpassword'})
        self.assertFalse(form.is_valid())
        

class BorrowFormTest(TestCase):
    def test_form_valid_data(self):
        form = BorrowForm(data={'DueDate': '2024-12-31'})

        self.assertTrue(form.is_valid())

    def test_due_date_invalid(self):
        form1 = BorrowForm(data={
            'DueDate': '2020-01-01' 
        })

        form2 = BorrowForm(data={
            'DueDate': timezone.now().date()
        })
        self.assertFalse(form1.is_valid())
        self.assertIn('Due date cannot be in the past or before the loan date.', form1.errors['DueDate'])
        self.assertFalse(form2.is_valid())
        self.assertIn('Due date cannot be the same as the loan date.', form2.errors['DueDate'])

    
    