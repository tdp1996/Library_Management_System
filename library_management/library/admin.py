from django.contrib import admin
from django.utils.html import format_html
from .models import Book, Member, Loan

class BookAdmin(admin.ModelAdmin):
    list_display = ("thumbnail","BookID", "ISBN", "Book_Title", "Book_Author", "Year_Of_Publication", "Publisher", "Genre", "Amount", "Available")
    def thumbnail(self, obj):
        if obj.Image_URL_S:
            return format_html('<img src="{}" width="50" height="75" />'.format(obj.Image_URL_S))
        return "No Image"
    thumbnail.short_description = 'Thumbnail'

class MemberAdmin(admin.ModelAdmin):
    list_display = ("MemberID", "Member_Name", "Gender", "Email", "Phone", "Member_Address", "JoinDate")

class LoanAdmin(admin.ModelAdmin):
    list_display = ("LoanID", "BookID", "MemberID", "LoanDate", "DueDate", "ReturnDate", "Loan_Status", "Fine")

admin.site.register(Book)
admin.site.register(Member, MemberAdmin)
admin.site.register(Loan, LoanAdmin)
