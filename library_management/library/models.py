from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

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

class MemberManager(BaseUserManager):
    def create_user(self, Email, Member_Name, Phone, Member_Address, password=None):
        if not Email:
            raise ValueError('Users must have an email address')
        user = self.model(
            Email=self.normalize_email(Email),
            Member_Name=Member_Name,
            Phone=Phone,
            Member_Address=Member_Address,
        )
        user.set_password(password)  # Thiết lập mật khẩu
        user.save(using=self._db)
        return user

    def create_superuser(self, Email, Member_Name, Phone, Member_Address, password):
        user = self.create_user(
            Email=Email,
            password=password,
            Member_Name=Member_Name,
            Phone=Phone,
            Member_Address=Member_Address,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Member(AbstractBaseUser):
    MemberID = models.AutoField(primary_key=True)
    Member_Name = models.CharField(max_length=100)
    Email = models.EmailField(unique=True)
    Phone = models.CharField(max_length=15)
    Member_Address = models.CharField(max_length=50)
    JoinDate = models.DateField(auto_now_add=True)
    
    # Thêm trường password từ AbstractBaseUser
    password = models.CharField(max_length=128, null=True)

    USERNAME_FIELD = 'Email'
    REQUIRED_FIELDS = ['Member_Name', 'Phone', 'Member_Address']

    objects = MemberManager()

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
