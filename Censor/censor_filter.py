from django import template

register = template.Library()

@register.filter
def censor(value):
    # Список нежелательных слов
    undesirable_words = ['плохое_слово1', 'плохое_слово2', 'плохое_слово3']
    for word in undesirable_words:
        value = value.replace(word, '*' * len(word))
    return value