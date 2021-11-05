from django import template
from django.db.models import Count

from serials.models import Category, TVSeries

register = template.Library()


@register.simple_tag()
def get_categories():
    """Show all categories."""
    return Category.objects.all()


@register.inclusion_tag('serials/tags/last_serials.html')
def show_last_serials(count=5):
    """Show the latest added TV series."""
    serials = TVSeries.objects.filter(is_published=True).order_by('-id')[:count]
    return {'last_serials': serials}


@register.inclusion_tag('serials/tags/most_commented_serials.html')
def get_most_commented_serials(count=5):
    """Show the most commented serials."""
    serials = TVSeries.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    return {'most_commented_serials': serials}


@register.simple_tag(takes_context=True)
def activate_on(context, name):
    """Render one active item on menu."""
    if context['request'].resolver_match.url_name == name:
        return 'active'
    return ''
