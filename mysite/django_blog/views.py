from django.views.generic import ListView
from django_blog.models import Article

class ArticlesListView(ListView):
    model = Article
    template_name = 'django_blog/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return (
            Article.objects
            .select_related('author', 'category')
            .prefetch_related('tags')
            .defer('content')
        )
