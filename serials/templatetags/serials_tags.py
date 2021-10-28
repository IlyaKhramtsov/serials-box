from django import template

from serials.models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    """Show all categories."""
    return Category.objects.all()
