from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('', views.main, name='main'),
    path('search/', views.search_books, name='search_books'),
    path('category/<str:genre>/', views.category_books, name='category_books'),
    path('library/details/<int:id>', views.details, name='details'),
]
