# Django React Components

Django React Components is a collection of tools that automate the loading and rendering of React components when used in
conjunction with django-react-compiler. This tool is currently in beta. 

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
- [`django-react-compiler`](https://github.com/zagaran/django-react-compiler): the JS counterpart to this
package, used to serve the React components for `django-react-components` to load into Django templates.
- [`django-webpack-loader`](https://github.com/owais/django-webpack-loader/): the Django dependency used to render the
runtime bundles required for React to run.
- [`webpack-bundle-tracker`](https://github.com/owais/webpack-bundle-tracker): the dependency used by Webpack to
generate stats to be consumed by `django-webpack-loader`.

## Usage

#### Rendering React Components

In your templates, you can render React components by using the `{% react_component %}` template tag.
```python
{% load react_component from django_react_components %}

{% react_component 'App' id='app' props=props %}
```

## Requirements

Python 3.4-3.7, Django 1.11-2.2
