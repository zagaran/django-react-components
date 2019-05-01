import json

from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def react_component(comp, **kwargs):
    if 'id' in kwargs:
        html_id = kwargs['id']
    else:
        html_id = comp
        kwargs['id'] = comp
    props = json.dumps(kwargs).replace("</", "<\\/").replace("\\", "\\\\")
    response = format_html("<div id='{html_id}'></div><script type='text/javascript'>window.reactComponents.{comp}.init('{props}');window.reactComponents.{comp}.render()</script>", html_id=html_id, comp=comp, props=mark_safe(props))
    return response
