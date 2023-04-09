from django.urls import path
from gutenberg_api import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('Books/', views.RedirectionBooks.as_view()),
    path('Books/<int:id>/', views.RedirectionDetailBook.as_view()),
    path('Books/search/<str:word>', views.RedirectionSimpleSearchBook.as_view()),
]
