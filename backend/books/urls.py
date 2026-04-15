from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.get_books),
    path('books/<int:pk>/', views.get_book),
    path('books/add/', views.add_book),

    path('ask/', views.ask_question),
    path('recommend/<int:book_id>/', views.get_recommendations),

    path('summary/', views.generate_summary_view),
    path('genre/', views.classify_genre),

    path('upload/', views.upload_books),
]