# Django React Components

Django React Components is a collection of tools that automate the loading and rendering of React components when used in
conjunction with `django-react-loader`. This tool is currently in beta. 

## Installation

Install `django-react-components` and [`django-webpack-loader`](https://github.com/owais/django-webpack-loader/) using pip:
```bash
$ pip install django-react-components django-webpack-loader
```
Add both modules to your `INSTALLED_APPS` in `settings.py`:
```python
INSTALLED_APPS = (
    ...,
    'django_react_components',
    'webpack_loader',
)
```
## Requirements

### Python
`django-react-components` relies on the [`django-webpack-loader`](https://github.com/owais/django-webpack-loader/) python module. Install it with `pip`:

```bash
$ pip install django-webpack-loader
```

### Javascript

#### Global

`django-react-components` uses `nwb` to compile compile React components. Install it globally:

```bash
$ npm install -g nwb
```
_or_
```bash
$ yarn global add nwb
```
 
 #### Local
 
 `django-react-components` uses [`webpack-bundle-tracker`](https://github.com/owais/webpack-bundle-tracker) and a sibling package, [`django-react-loader`](https://github.com/zagaran/django-react-loader), to generate and render the react components. Install them locally:
 
 ```bash
$ npm install --save-dev django-react-loader webpack-bundle-tracker
```
_or_
```bash
$ yarn add django-react-loader webpack-bundle-tracker --dev
```

## Usage

### Configuration

You will need to create a file called `nwb.config.js` to configure `nwb` to properly compile your components. Check out `nwb`'s (configuration guide)[https://github.com/insin/nwb/blob/master/docs/Configuration.md#configuration-file] for more details. Also look at their (webpack configuration options)[https://github.com/insin/nwb/blob/master/docs/Configuration.md#webpack-configuration]. 

In your config file, add `django-react-loader` as a loader to the webpack section of it. For example:

```js
// nwb.config.js

module.exports = {
  webpack: {
    ...,
    module: {
      rules: [
        {
          loader: ['django-react-loader'],
        },
      ],
    },
  }
};
```

The loader will run on every entry passed to the nwb config file. For example, if you wanted to load three react components:

```js
Comp1.js
Comp2.js
Comp3.js
```

your config file might look like this: 
```js
//nwb.config.js

module.exports = {
  webpack: {
    ...,
    entry: {
      Comp1: './src/Comp1.js',
      Comp2: './src/Comp2.js',
      Comp3: './src/Comp3.js'
    },
  }
};
```

The default export of each entry point will be compiled and attached to window on load using the key of the entry point in the config file, so in out example,:
```js
window.Comp1 // The component at './src/Comp1.js'
window.Comp2 // The component at './src/Comp2.js'
window.Comp1 // The component at './src/Comp3.js'
```

The template tags from `django-react-components` will run an initialization function on the code attached to window to create the component using the props provided to the template.

### Setting up `webpack-bundle-tracker`

You will also need to specify the locations to bundle the javascript with the `webpack-bundle-tracker`. For example:
```js
var path = require('path')
var BundleTracker = require('webpack-bundle-tracker')
module.exports = {
  webpack: {
    ...,
    output: {
      path: path.resolve('./dist/webpack_bundles/'), // Location for compiled files
    },
    plugins: [
      new BundleTracker({filename: './webpack-stats.json'}), // Location for generated tracking file
    ],
  }
};
```
### Compiling React Components

Compile your react source code with `nwb`. Make sure to include the `-no-vendor` flag:

```bash
nwb build --no-vendor
```

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
    {% react_component 'App' id='app' prop1=prop1 prop2=prop2 %}
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
class with the `DJANGO_REACT_JSON_ENCODER` settings in your settings file. It will be passed to `json.dumps(props, cls=MyJSONEncoder)`

## Requirements

Python 3.4-3.7, Django 1.11-2.2
