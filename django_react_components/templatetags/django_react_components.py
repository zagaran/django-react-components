"""
Template tags for django-react-components
"""
import uuid

from django import template
from django.conf import settings
from django.template import TemplateSyntaxError
from django.template.base import token_kwargs
from django.utils.html import format_html, json_script
from django.utils.module_loading import import_string

register = template.Library()

encoder_class_import_string = getattr(settings, "DJANGO_REACT_JSON_ENCODER", "django.core.serializers.json.DjangoJSONEncoder")
if not isinstance(encoder_class_import_string, str):
    raise ImportError("DJANGO_REACT_JSON_ENCODER must be set as an import string.")
else:
    encoder_class = import_string(encoder_class_import_string)


@register.simple_tag
def react_component(component_name, component_id=None, props=None, **kwargs):
    """
    Render a React component with kwargs as attributes. This current requires that all kwargs
    being passed in be JSON-serializable.
    """
    if component_id is None:
        component_id = str(uuid.uuid4())
    if props is None:
        props = {}
    props.update(id=component_id)
    props.update(kwargs)
    props_id = component_id+'_props'

    react_component_html = """
        <div id="{html_id}"></div>
        {props} 
        <script type="text/javascript">
            window.reactComponents.{component_name}.init(document.getElementById("{props_id}").textContent)
            window.reactComponents.{component_name}.render()
        </script>
    """

    return format_html(
        react_component_html,
        props_id=props_id,
        props=json_script(props, props_id, encoder=encoder_class),
        html_id=component_id,
        component_name=component_name,
    )


class ReactBlockNode(template.Node):
    def __init__(self, component, nodelist, component_id=None, props=None, **kwargs):
        if component_id is None:
            component_id = str(uuid.uuid4())
        self.component = component
        self.html_id = component_id
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
        props_id = html_id + '_props'

        react_component_html = """
            <div id="{html_id}"></div>
            {props}
            <script type="text/javascript">
                window.reactComponents.{component}.init(document.getElementById("{props_id}").textContent)
                window.reactComponents.{component}.render()
            </script>
        """
        return format_html(
            react_component_html,
            props=json_script(resolved_props, props_id, encoder=encoder_class),
            props_id=props_id,
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
