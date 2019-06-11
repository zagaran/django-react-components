"""
Template tags for django-react-components
"""
import json
import uuid

from django import template
from django.template import TemplateSyntaxError
from django.template.base import token_kwargs
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


class ReactBlockNode(template.Node):
    def __init__(self, component, html_id, nodelist, **kwargs):
        self.component = component
        self.html_id = html_id
        self.props = kwargs
        self.nodelist = nodelist

    def render(self, context):
        component = self.component.resolve(context)
        html_id = self.html_id.resolve(context)
        resolved_props = {key: prop.resolve(context) for key, prop in self.props.items()}
        resolved_props['children'] = self.nodelist.render(context)
        serialized_props = json.dumps(resolved_props).replace("</", "<\\/").replace("\\", "\\\\")
        react_component_html = """
            <div id="{html_id}"></div>
            <script type="text/javascript">
                window.reactComponents.{component}.init('{props}')
                window.reactComponents.{component}.render()
            </script>
        """
        return format_html(
            react_component_html,
            props=mark_safe(serialized_props),
            html_id=html_id,
            component=component
        )


@register.tag(name='react')
def do_react_block(parser, token):
    """
    Render a React component with kwargs as attributes. This current requires that all kwargs
    being passed in be JSON-serializable.
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument, a React component name." % bits[0])

    component = parser.compile_filter(bits[1])
    remaining_bits = bits[2:]
    kwargs = token_kwargs(remaining_bits, parser)
    if remaining_bits:
        raise TemplateSyntaxError("%r received an invalid token: %r" %
                                  (bits[0], remaining_bits[0]))

    nodelist = parser.parse(('endreact',))
    parser.delete_first_token()

    if 'id' not in kwargs:
        kwargs['id'] = str(uuid.uuid4())

    return ReactBlockNode(component, kwargs['id'], nodelist, **kwargs)
