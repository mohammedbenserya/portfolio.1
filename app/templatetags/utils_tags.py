# app/templatetags/utils_tags.py

from django import template
from app.services.utils import sync_translate

register = template.Library()

@register.simple_tag
def trans_req_tag(text, lang):
    return sync_translate(text, lang)