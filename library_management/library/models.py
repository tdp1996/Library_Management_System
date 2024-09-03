from django.db import models

class Book(models.Model):
    BookID = models.AutoField(primary_key=True)
    ISBN = models.CharField(max_length=20, unique=True)
    Book_Title = models.CharField(max_length=100)
    Book_Author = models.CharField(max_length=50, blank=True, null=True)
    Year_Of_Publication = models.IntegerField(blank=True, null=True)
    Publisher = models.CharField(max_length=50, blank=True, null=True)
    Genre = models.CharField(max_length=50, blank=True, null=True)
    Amount = models.IntegerField()
    Available = models.IntegerField()
    Image_URL_S = models.URLField(max_length=255, blank=True, null=True)
    Image_URL_M = models.URLField(max_length=255, blank=True, null=True)
    Image_URL_L = models.URLField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Books'

class Member(models.Model):
    MemberID = models.AutoField(primary_key=True)
    Member_Name = models.CharField(max_length=100)
    Gender = models.CharField(max_length=10)
    Email = models.EmailField()
    Phone = models.CharField(max_length=15)
    Member_Address = models.CharField(max_length=50)
    JoinDate = models.DateField()

    class Meta:
        db_table = 'Members'

class Loan(models.Model):
    LoanID = models.AutoField(primary_key=True)
    BookID = models.ForeignKey(Book, on_delete=models.CASCADE)
    MemberID = models.ForeignKey(Member, on_delete=models.CASCADE)
    LoanDate = models.DateField()
    DueDate = models.DateField()
    ReturnDate = models.DateField(blank=True, null=True)
    Loan_Status = models.CharField(max_length=20, default='On Loan')
    Fine = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'Loans'
