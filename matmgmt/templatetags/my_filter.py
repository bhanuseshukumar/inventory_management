from django import template

register = template.Library()

@register.filter
def get_at_index(list, index_arg):
    return list[index_arg]