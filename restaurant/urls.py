from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book, name='book'),
    path('bookings/', views.bookings, name='bookings'),
]
