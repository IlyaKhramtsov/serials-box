from django import template
from django.shortcuts import get_object_or_404

from blog.models import Article

register = template.Library()


@register.simple_tag()
def is_liked(*args, **kwargs):
    article = get_object_or_404(Article, slug=kwargs['slug'])
    return article.likes.filter(id=kwargs['user_id']).exists()


@register.simple_tag()
def total_likes(*args, **kwargs):
    article = get_object_or_404(Article, slug=kwargs['slug'])
    return article.total_likes()
