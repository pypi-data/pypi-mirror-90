# ustache

Mustache for Python.

Documentation: [ustache.readthedocs.io](https://ustache.readthedocs.io)

## Usage

```python
import ustache

print(ustache.render('Hello {{v}}', {'v': 'World!'}))
# Hello World!
```

Command line:

```console
$ ustache -j data.json -o output.html template.mustache
```

## Highlights

- Command line interface.
- Spec compliant, but also highly compatible with `Mustache.js`.
- Fast and small codebase, efficiently rendering to str or bytes,
  supporting streaming.
- Customizable (property getter, partial resolver, and stringify, escape
  and lambda render functions).

## Considerations

For inter-compatibility with JavaScript (enabling client-side rendering with
the same templates), ustache made some deliberate behavior choices:

- Mustache blocks stick to JavaScript falseness (`__bool__` is not honored):
  `None`, `False`, `0`, `nan`, and empty sequences (including strings)
  are taken as falsy, while everything else (including empty mappings) will
  be considered truthy (Mustache.js `Boolean` and empty `Array` handling).
- Mustache blocks receiving any iterable other than mappings and strings
  will result on a loop (Mustache.js `Array` handling).
- Sequences expose a virtual `length` property
  (JavaScript `Array.length` emulation).
- Sequence elements are accessible by positive index in the same way mapping
  integer-keyed items are also accessible if no string key conflicts, as
  properties (JavaScript `Object` emulation).

## Syntax

Check out the [mustache(5) manual](https://mustache.github.io/mustache.5.html).

For quick reference, here is a quick overview of the Mustache syntax.

Template:
```mustache
{{!comment}}
<ul>
{{#object}}<li>{{property}}</li>{{/object}}
{{^object}}<li>As <b>object</b> is truthy, this won't be shown</li>{{/object}}
{{^null}}<li><b>null</b> is falsy</li>{{/null}}
{{#array}}<li>{{property}}</li>
{{/array}}
{{^array}}<li>Array isn't empty, this won't be shown.</li>{{/array}}
{{#empty_array}}<li>Empty Array, this won't be shown</li>{{/empty_array}}
{{^empty_array}}<li>empty_array is empty</li>{{/empty_array}}
{{&unescaped_html}}
</ul>
```

Data:
```json
{
  "object": {
    "property": "Object property value"
  },
  "null": null,
  "array": [
    {"property": "Array item1 property"},
    {"property": "Array item2 property"},
    {"property": "Array item3 property"}
  ],
  "empty_array": [],
  "unescaped_html": "<li>this is unescaped html</li>"
}
```

Output:
```html
<ul>
<li>Object property value</li>
<li><b>null</b> is falsy</li>
<li>Array item1 property</li>
<li>Array item2 property</li>
<li>Array item3 property</li>
<li>empty_array is empty</li>
<li>this is unescaped html</li>
</ul>
```
