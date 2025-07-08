# Django React Components

`django-react-components` and it's sibling package `django-react-loader` facilitate using individual react components
in a django template with a simple template tag.  This also webpack, and the paired packages `webpack-bundle-tracker` 
and `django-webpack-loader` to compile the react components and make them available within django. 

## Installation

For normal usage, first install `django-react-components` using pip:
```bash
$ pip install django-react-components
```
Add 'django_react_components' and 'webpack_loader'  modules to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = (
    ...,
    'django_react_components',
    'webpack_loader',
)
```

## Additional Requirements

Install Webpack 5 [Installation Guide](https://webpack.js.org/guides/installation/)
The command may resemble: 

```bash
npm install --save-dev webpack
```

Install `django-react-loader` with your preferred package manager: 

```bash
$ npm install --save-dev django-react-loader 
```
_or_
```bash
$ yarn add django-react-loader --dev
```

## Usage

### Configuration

Configure Webpack: [Webpack Configuration Guide](https://webpack.js.org/configuration/).  The rest of this guide assumes a webpack config file (probably called `webpack.config.js`)

#### Setting up `django-webpack-loader` and `webpack-bundle-tracker`

Follow instructions in the [Django Webpack Loader Docs](https://github.com/django-webpack/django-webpack-loader)

#### Setting up `django-react-loader`

Modify the webpack config file so that `django-react-loader` loads the react files: 
    * Import the django-react-loader
    * Specify ENTRIES - a mapping of the names of your components to the source code file
    * Add `django-react-loader` to loaders

Example configuration outline: 

```js
    //wepback.config.js
    const DjangoReactLoader = require('django-react-loader');
    ...,
    const ENTRIES = {
        ...,
        nameOfComponent: componentImportPath

    }
    ...,

    module.exports = {
        ...,
        module: {
            rules: [
                ...,
                {
                 test: /\.js$/,
                 exclude: /node_modules/,
                 options: {
                   entries: ENTRIES
                 },
                 loader: DjangoReactLoader 
               }
    ...,
```

### Compiling React Components

Compile your react components with `webpack`. 

Command likely to resemble ```webpack build``` 


### Rendering React Components

In your templates, you can render React components by using the `{% react_component %}` or the `{% react %}`template tag. To do so:

1. Load the template tag and the `render_bundle` tag from `django_webpack_loader`:
```python
{% load django_react_components %}
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
    {% react_component 'App' component_id='app' prop1=prop1 prop2=prop2 %}
</body>
```

3b. Use the `react`/`endreact` tags to render the component with rendered content inside. This will be passed as raw HTML to the component as the `children` prop.
```
<body>
    {% react 'App' id='app' %}
        <h1>Hello World</h1>
        <p>{{ content }}</p>
        <a href='{% url 'endpoint' %}'>Link</a>
    {% endreact 'App' id='app' %}
</body>
```

### Custom Props Encoding

`django_react_components` uses JSON to encode props into the React components. You can specify a custom JSON encoder 
class with the `DJANGO_REACT_JSON_ENCODER` settings in your settings file, otherwise the default DjangoJSONEncoder is used.
The encoder will be passed to `json_script()`

## Requirements

Python 3.11, Django 4.2
