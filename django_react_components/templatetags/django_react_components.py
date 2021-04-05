"""
Template tags for django-react-components
"""
import json
import uuid

from django import template
from django.conf import settings
from django.template import TemplateSyntaxError
from django.template.base import token_kwargs
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe

register = template.Library()

encoder_class_import_string = getattr(settings, "DJANGO_REACT_JSON_ENCODER", "django.core.serializers.json.DjangoJSONEncoder")
if not isinstance(encoder_class_import_string, str):
    raise ImportError("DJANGO_REACT_JSON_ENCODER must be set as an import string.")
else:
    encoder_class = import_string(encoder_class_import_string)


def initialize_props(props, html_id=None):
    """Initialize is and props."""
    if html_id is None:
        html_id = str(uuid.uuid4())
    if props is None:
        props = {}
    if "html_id" not in props:
        props.update(html_id=html_id)
    return props


@register.simple_tag
def react_widget(component_name, html_id=None, props=None, **kwargs):
    """
    Render a standalone react widget, including boilerplate loading code. This currently requires
    all kwargs beings passed to be JSON-serializable.
    """
    props = initialize_props(props, html_id=html_id)
    props.update(kwargs)
    return render_to_string(
        "django_react_components/react_widget.html",
        context={
            **props,
            "react_component_name": component_name
        }
    )


@register.simple_tag
def render_react(component_name, props=None):
    """
    Render a React component with kwargs as attributes. This currently requires that all kwargs
    being passed in be JSON-serializable.
    """
    props = initialize_props(props)
    html_id = props["html_id"]
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
        html_id=html_id,
        component_name=component_name,
    )


class ReactBlockNode(template.Node):
    def __init__(self, component, nodelist, html_id=None, props=None, **kwargs):
        if html_id is None:
            html_id = str(uuid.uuid4())
        self.component = component
        self.html_id = html_id
        self.props = props
        self.kwargs = kwargs
        self.nodelist = nodelist

    def render(self, context):
        component = self.component.resolve(context)
        html_id = self.html_id.resolve(context)
        resolved_props = {key: value.resolve(context) for key, value in self.kwargs.items()}
        if self.props is not None:
            resolved_props.update(self.props.resolve(context))
        resolved_props['html_id'] = html_id
        resolved_props['children'] = self.nodelist.render(context)
        return render_to_string(
            "django_react_components/react_widget.html",
            context={
                **resolved_props,
                "react_component_name": component
            }
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
