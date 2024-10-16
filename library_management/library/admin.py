from django.contrib import admin
from django.utils.html import format_html
from .models import Book, Member, Loan
from .models import Member, Loan
from django.contrib.auth.admin import UserAdmin
from .forms import MemberCreationForm, MemberChangeForm

class BookAdmin(admin.ModelAdmin):
    list_display = ("thumbnail","BookID", "ISBN", "Book_Title", "Book_Author", "Year_Of_Publication", "Publisher", "Genre", "Amount", "Available")
    search_fields = ('Book_Title', 'ISBN', 'Book_Author', 'Genre')
    def thumbnail(self, obj):
        if obj.Image_URL_S:
            return format_html('<img src="{}" width="50" height="75" />'.format(obj.Image_URL_S))
        return "No Image"
    thumbnail.short_description = 'Thumbnail'



class MemberAdmin(UserAdmin):
    add_form = MemberCreationForm
    form = MemberChangeForm
    model = Member
    list_display = ('Email', 'Name', 'Phone', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('Email', 'password')}),
        ('Personal Info', {'fields': ('Name', 'Phone', 'Address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('Email', 'Name', 'Phone', 'Address', 'password1', 'password2')}
        ),
    )
    search_fields = ('Email',)
    ordering = ('Email',)

class LoanAdmin(admin.ModelAdmin):
    list_display = ("LoanID", "BookID", "MemberID", "LoanDate", "DueDate", "ReturnDate", "Loan_Status", "Fine")

admin.site.register(Book, BookAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Loan, LoanAdmin)
admin.site.site_header = "Library Management System Admin"
admin.site.site_title = "LMS Admin Portal"
admin.site.index_title = "Welcome to LMS Admin"

