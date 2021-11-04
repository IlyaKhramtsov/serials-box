from django import template

from serials.models import Category, TVSeries

register = template.Library()


@register.simple_tag()
def get_categories():
    """Show all categories."""
    return Category.objects.all()


@register.inclusion_tag('serials/tags/last_serials.html')
def show_last_serials(count=5):
    serials = TVSeries.objects.filter(is_published=True).order_by("-id")[:count]
    return {"last_serials": serials}
