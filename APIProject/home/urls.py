from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from home import views

urlpatterns = [
    path('snippets/', views.SnippetList.as_view()),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
]