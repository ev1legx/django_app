from django.urls import path
from django_blog.views import ArticlesListView

urlpatterns = [
    path('', ArticlesListView.as_view(), name='article-list'),
]
