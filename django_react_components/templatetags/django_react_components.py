"""
Template tags for django-react-components
"""
import json
import uuid

from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def react_component(component_name, **kwargs):
    """
    Render a React component with kwargs as attributes. This current requires that all kwargs
    being passed in be JSON-serializable.
    """
    kwargs['id'] = kwargs.get('id', str(uuid.uuid4()))
    props = json.dumps(kwargs).replace("</", "<\\/").replace("\\", "\\\\")
    
    react_component_html = """
        <div id="{html_id}"></div>
        <script type="text/javascript">
            window.reactComponents.{component_name}.init('{props}')
            window.reactComponents.{component_name}.render()
        </script>
    """
    
    return format_html(
        react_component_html,
        props=mark_safe(props),
        html_id=kwargs['id'],
        component_name=component_name,
    )
