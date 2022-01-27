from django import template
from django.db.models import Count

from serials.models import TVSeries

register = template.Library()


@register.inclusion_tag('serials/tags/last_serials.html')
def show_last_serials(count=5):
    """Show the latest added TV series."""
    serials = TVSeries.objects.filter(is_published=True).order_by('-id')[:count]
    return {'last_serials': serials}


@register.inclusion_tag('serials/tags/most_commented_serials.html')
def get_most_commented_serials(count=5):
    """Show the most commented serials."""
    serials = (
        TVSeries.objects
        .annotate(total_comments=Count('comments'))
        .select_related('category')
        .order_by('-total_comments')[:count]
    )
    return {'most_commented_serials': serials}
