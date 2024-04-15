from taggit.models import Tag

from .models import Category, Posts


def category(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return context


def post_tags(request):
    posts = Posts.published.prefetch_related('tags').all()
    tags = Tag.objects.all()
    context = {
        'posts': posts,
        'tags': tags
    }
    return context
