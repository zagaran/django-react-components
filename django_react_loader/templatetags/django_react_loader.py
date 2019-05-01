import json
import uuid

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def react_component(component_name, **kwargs):
    """
    Render a React component with kwargs as attributes. This current requires that all kwargs
    being passed in be JSON-serializable.
    """
    component_name = conditional_escape_json(component_name)
    kwargs['id'] = kwargs.get('id', str(uuid.uuid4()))
    
    kwargs_safe = mark_safe(
        json.dumps(
            {conditional_escape_json(key): conditional_escape_json(value)
             for key, value in kwargs.items()}
        )
    )
    react_component_html = f"""
        <span>1</span>
        <div id="{kwargs['id']}"></div>
        <script type="text/javascript">
            window.reactComponents.{component_name}.init('{kwargs_safe}')
            window.reactComponents.{component_name}.render()
        </script>
    """
    return mark_safe(react_component_html)


def conditional_escape_json(obj):
    """
    Conditionally escape json-like object such that it retains its data type and will only run
    mark_safe on strings.
    """
    if isinstance(obj, dict):
        return {
            conditional_escape_json(key): conditional_escape_json(value)
            for key, value in obj.items()
        }
    elif isinstance(obj, list):
        return [conditional_escape_json(item) for item in obj]
    elif isinstance(obj, str):
        return conditional_escape(obj)
    else:
        return obj
