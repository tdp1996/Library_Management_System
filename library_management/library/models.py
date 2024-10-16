from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class Book(models.Model):
    BookID = models.AutoField(primary_key=True)
    ISBN = models.CharField(max_length=20, unique=True)
    Book_Title = models.CharField(max_length=100)
    Book_Author = models.CharField(max_length=50)
    Year_Of_Publication = models.IntegerField()
    Publisher = models.CharField(max_length=50)
    Genre = models.CharField(max_length=50)
    Amount = models.IntegerField(null=True)
    Available = models.IntegerField(null=True)
    Image_URL_S = models.URLField(max_length=255, blank=True, null=True)
    Image_URL_M = models.URLField(max_length=255, blank=True, null=True)
    Image_URL_L = models.URLField(max_length=255, blank=True, null=True)
    PDF_Link = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'Books'

class MemberManager(BaseUserManager):
    def create_user(self, Email, Name, Phone, Address, password=None):
        if not Email:
            raise ValueError('Users must have an email address')
        user = self.model(
            Email=self.normalize_email(Email),
            Name=Name,
            Phone=Phone,
            Address=Address,
        )
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, Email, Name, Phone, Address, password):
        user = self.create_user(
            Email=Email,
            password=password,
            Name=Name,
            Phone=Phone,
            Address=Address,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Member(AbstractBaseUser, PermissionsMixin):
    MemberID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Email = models.EmailField(unique=True) 
    Phone = models.CharField(max_length=15)
    Address = models.CharField(max_length=50)
    JoinDate = models.DateField(auto_now_add=True)

    # Status fields required by Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    class Meta:
        db_table = 'Members'

    USERNAME_FIELD = 'Email'
    REQUIRED_FIELDS = ['Name', 'Phone', 'Address']

    objects = MemberManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Loan(models.Model):
    LoanID = models.AutoField(primary_key=True)
    BookID = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='BookID')
    MemberID = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='MemberID')
    LoanDate = models.DateField()
    DueDate = models.DateField()
    ReturnDate = models.DateField(blank=True, null=True)
    Loan_Status = models.CharField(max_length=20, default='On Loan')
    Fine = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'Loans'
