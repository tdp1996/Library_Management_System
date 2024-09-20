from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('search/', views.search_books, name='search_books'),
    path('category/<str:genre>/', views.category_books, name='category_books'),
    path('category/details/<int:id>', views.details, name='details'),
    path('register/', views.register, name='register'),
    path('login/', views.member_login, name='login'),
    path('member_profile/<int:id>/', views.member_profile, name='member_profile'),
    path('logout/', views.logout_view, name='logout'),
]
