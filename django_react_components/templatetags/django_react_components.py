"""
Template tags for django-react-components
"""
import json
import uuid

from django import template
from django.conf import settings
from django.template import TemplateSyntaxError
from django.template.base import token_kwargs
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()

encoder_class = getattr(settings, "DJANGO_REACT_JSON_ENCODER", None)

@register.simple_tag
def react_component(component_name, id=None, props=None, **kwargs):
    """
    Render a React component with kwargs as attributes. This current requires that all kwargs
    being passed in be JSON-serializable.
    """
    if id is None:
        id = str(uuid.uuid4())
    if props is None:
        props = {}
    props.update(id=id)
    props.update(kwargs)
    json_props = json.dumps(props, cls=encoder_class).replace("</", "<\\/").replace("\\", "\\\\").replace("'", "\\'")
    react_component_html = """
        <div id="{html_id}"></div>
        <script type="text/javascript">
            window.reactComponents.{component_name}.init('{props}')
            window.reactComponents.{component_name}.render()
        </script>
    """

    return format_html(
        react_component_html,
        props=mark_safe(json_props),
        html_id=id,
        component_name=component_name,
    )


class ReactBlockNode(template.Node):
    def __init__(self, component, nodelist, id=None, props=None, **kwargs):
        if id is None:
            id = str(uuid.uuid4())
        self.component = component
        self.html_id = id
        self.props = props
        self.kwargs = kwargs
        self.nodelist = nodelist

    def render(self, context):
        component = self.component.resolve(context)
        html_id = self.html_id.resolve(context)
        resolved_props = {key: value.resolve(context) for key, value in self.kwargs.items()}
        if self.props is not None:
            resolved_props.update(self.props.resolve(context))
        resolved_props['id'] = html_id
        resolved_props['children'] = self.nodelist.render(context)
        json_props = json.dumps(resolved_props, cls=encoder_class).replace("</", "<\\/").replace("\\", "\\\\").replace("'", "\\'")
        react_component_html = """
            <div id="{html_id}"></div>
            <script type="text/javascript">
                window.reactComponents.{component}.init('{props}')
                window.reactComponents.{component}.render()
            </script>
        """
        return format_html(
            react_component_html,
            props=mark_safe(json_props),
            html_id=html_id,
            component=component
        )


@register.tag(name='react')
def do_react_block(parser, token):
    """
    Render a React component with kwargs as attributes. This currently requires that all kwargs
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
    return ReactBlockNode(component, nodelist, **kwargs)
