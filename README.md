# Django React Components

Django React Components is a collection of tools that automate the loading and rendering of React components when used in
conjunction with `django-react-loader`. This tool is currently in beta. 

## Installation

Install Django React Components using pip:
```bash
$ pip install django-react-components
```
Add `django_react_components` to your `INSTALLED_APPS` in `settings.py`:
```python
INSTALLED_APPS = (
    ...,
    'django_react_components',
)
```

You will also need to install three other dependencies:
- [`django-react-loader`](https://github.com/zagaran/django-react-loader): the JS counterpart to this
package, used to serve the React components for `django-react-components` to load into Django templates.
- [`django-webpack-loader`](https://github.com/owais/django-webpack-loader/): the Django dependency used to render the
runtime bundles required for React to run.
- [`webpack-bundle-tracker`](https://github.com/owais/webpack-bundle-tracker): the dependency used by Webpack to
generate stats to be consumed by `django-webpack-loader`.

## Usage

#### Rendering React Components

In your templates, you can render React components by using the `{% react_component %}` template tag. To do so:

1. Load the template tag and the `render_bundle` tag from `django_webpack_loader`:
```python
{% load react_component from django_react_components %}
{% load render_bundle from webpack_loader %}

```

2. Use `render_bundle` to pull in the appropriate javascript
```
<head>
    {% render_bundle 'runtime' %}
    {% render_bundle 'App' %} 
</head>
```

3a. Use the `react_component` tag to render the component with keyword arguments as props
```
<body>
    {% react_component 'App' id='app' prop1=prop1 prop2=prop2 %}
</body>
```

3a. Use the `react`/`endreact` tags to render the component with rendered content inside. This will be passed as raw HTML to the component as the `children` prop.
```
<body>
    {% react 'App' id='app' %}
        <h1>Hello World</h1>
        <p>{{ content }}</p>
        <a href='{% url 'endpoint' %}'>Link</a>
    {% endreact 'App' id='app' %}
</body>
```

## Requirements

Python 3.4-3.7, Django 1.11-2.2
