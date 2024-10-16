from django.test import TestCase
from django.utils import timezone
from ..models import Book, Member, Loan


class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            ISBN="1234567890",
            Book_Title="Test Book",
            Book_Author="Author",
            Year_Of_Publication=2024,
            Publisher="Publisher",
            Genre="Classic"
        )
        
    def test_book_creation(self):
        self.assertEqual(self.book.Book_Title, "Test Book")
        self.assertEqual(self.book.Book_Author, "Author")
        self.assertEqual(self.book.Year_Of_Publication, 2024)
        self.assertEqual(self.book.Publisher, "Publisher")
        self.assertEqual(self.book.Genre,"Classic")

class MemberModelTest(TestCase):
    def setUp(self):
        self.member = Member.objects.create_user(
            Email="testuser@example.com",
            Name="Test User",
            Phone="0123456789",
            Address="123 Street"
        )

    def test_member_creation(self):
        self.assertEqual(self.member.Email, "testuser@example.com")
        self.assertEqual(self.member.Name, "Test User")


class LoanModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            ISBN="1234567890",
            Book_Title="Sample Book",
            Book_Author="Author 1",
            Year_Of_Publication=2021,
            Publisher="Sample Publisher",
            Genre="Fiction",
            Amount=5,
            Available=5
        )
        
        self.member = Member.objects.create_user(
            Name="Test User",
            Email="testuser@example.com",
            Phone="0123456789",
            Address="123 Test Street",
            password="password123"
        )
    
    def test_create_loan(self):

        loan = Loan.objects.create(
            BookID=self.book,
            MemberID=self.member,
            LoanDate=timezone.now().date(),
            DueDate=timezone.now().date() + timezone.timedelta(days=7)
        )

        self.assertEqual(loan.BookID.Book_Title, "Sample Book")
        self.assertEqual(loan.MemberID.Email, "testuser@example.com")
        self.assertEqual(loan.Loan_Status, "On Loan")  
        self.assertIsNone(loan.ReturnDate) 
        self.assertEqual(self.book.Available, 5)

    def test_loan_book_updates_availability(self):
        loan = Loan.objects.create(
            BookID=self.book,
            MemberID=self.member,
            LoanDate=timezone.now().date(),
            DueDate=timezone.now().date() + timezone.timedelta(days=7)
        )
        loan.BookID.Available -= 1
        loan.BookID.save()

        self.assertEqual(loan.BookID.Available, 4)

    def test_return_book_updates_status_and_availability(self):
        loan = Loan.objects.create(
            BookID=self.book,
            MemberID=self.member,
            LoanDate=timezone.now().date(),
            DueDate=timezone.now().date() + timezone.timedelta(days=7)
        )

        loan.ReturnDate = timezone.now().date() + timezone.timedelta(days=7)
        loan.Loan_Status = "Returned"
        loan.BookID.Available += 1  
        loan.save()


        self.assertEqual(loan.Loan_Status, "Returned")
        self.assertEqual(loan.BookID.Available, 6)
        self.assertIsNotNone(loan.ReturnDate)

    def test_fine_calculation(self):
        loan = Loan.objects.create(
            BookID=self.book,
            MemberID=self.member,
            LoanDate=timezone.now().date() - timezone.timedelta(days=10),
            DueDate=timezone.now().date() - timezone.timedelta(days=5),
            ReturnDate=timezone.now().date(),
            Loan_Status="Returned"
        )

        days_overdue = (loan.ReturnDate - loan.DueDate).days
        fine_per_day = 1.00
        loan.Fine = days_overdue * fine_per_day
        loan.save()

        self.assertEqual(loan.Fine, days_overdue * fine_per_day)

