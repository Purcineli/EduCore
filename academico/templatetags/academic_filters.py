from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    '''Get an item from a dictionary. Tries integer key first, then string key.'''
    if dictionary is None:
        return None
    try:
        return dictionary[int(key)]
    except (TypeError, ValueError, KeyError):
        pass
    try:
        return dictionary.get(key)
    except AttributeError:
        return None
