squarify
========
![](https://img.shields.io/pypi/v/squarify.svg?style=flat)
![](https://github.com/laserson/squarify/actions/workflows/python-package.yml/badge.svg)
![](https://img.shields.io/pypi/pyversions/squarify.svg?style=flat)
![](https://img.shields.io/pypi/l/squarify.svg?style=flat)

Pure Python implementation of the squarify treemap layout algorithm.

Based on algorithm from [Bruls, Huizing, van Wijk, "Squarified Treemaps"](https://doi.org/10.1007/978-3-7091-6783-0_4), but
implements it differently.

## Contents

* [Installation](#Installation)
* [Usage](#Usage)
* [Example](#Example)
* [Documentation](#Documentation-for-Squarify)

Installation
------------

Compatible with Python 2 and Python 3.

    pip install squarify


Usage
-----

The main function is `squarify` and it requires two things:

* A coordinate system comprising values for the origin (`x` and `y`) and the
width/height (`dx` and `dy`).
* A list of positive values sorted from largest to smallest and normalized to
the total area, i.e., `dx * dy`).

The function returns a list of `dict`s (i.e., JSON objects), each one a
rectangle with coordinates corresponding to the given coordinate system and area
proportional to the corresponding value.  Here's an example rectangle:

```json
{
    "x": 0.0,
    "y": 0.0,
    "dx": 327.7,
    "dy": 433.0
}
```

The rectangles can be easily plotted using, for example,
[d3.js](http://d3js.org/).

There is also a version of `squarify` called `padded_squarify` that returns
rectangles that, when laid out, have a bit of padding to show their borders.

The helper function `normalize_sizes` will compute the normalized values, and
the helper function `plot` will generate a Matplotlib-based treemap
visualization of your data (see [documentation](#Documentation-for-Squarify)).


Example
-------
```python
import squarify

# these values define the coordinate system for the returned rectangles
# the values will range from x to x + width and y to y + height
x = 0.
y = 0.
width = 700.
height = 433.

values = [500, 433, 78, 25, 25, 7]

# values must be sorted descending (and positive, obviously)
values.sort(reverse=True)

# the sum of the values must equal the total area to be laid out
# i.e., sum(values) == width * height
values = squarify.normalize_sizes(values, width, height)

# returns a list of rectangles
rects = squarify.squarify(values, x, y, width, height)

# padded rectangles will probably visualize better for certain cases
padded_rects = squarify.padded_squarify(values, x, y, width, height)
```

The variable `rects` contains

```json
[
  {
    "dy": 433,
    "dx": 327.7153558052434,
    "x": 0,
    "y": 0
  },
  {
    "dy": 330.0862676056338,
    "dx": 372.2846441947566,
    "x": 327.7153558052434,
    "y": 0
  },
  {
    "dy": 102.9137323943662,
    "dx": 215.0977944236371,
    "x": 327.7153558052434,
    "y": 330.0862676056338
  },
  {
    "dy": 102.9137323943662,
    "dx": 68.94160077680677,
    "x": 542.8131502288805,
    "y": 330.0862676056338
  },
  {
    "dy": 80.40135343309854,
    "dx": 88.24524899431273,
    "x": 611.7547510056874,
    "y": 330.0862676056338
  },
  {
    "dy": 22.51237896126767,
    "dx": 88.2452489943124,
    "x": 611.7547510056874,
    "y": 410.4876210387323
  }
]
```

Documentation for [Squarify](squarify/__init__.py)
---------

`normalize_sizes(sizes, dx, dy)`
:   Normalize list of values.

Normalizes a list of numeric values so that `sum(sizes) == dx * dy`.

**Parameters**

    sizes : list-like of numeric values
        Input list of numeric values to normalize.
    dx, dy : numeric
        The dimensions of the full rectangle to normalize total values to.

    Returns
    -------
    list[numeric]
        The normalized values.

----------------------------------------------------------------------------------------

`padded_squarify(sizes, x, y, dx, dy)`
:   Compute padded treemap rectangles.

See `squarify` docstring for details. The only difference is that the
returned rectangles have been "padded" to allow for a visible border.

----------------------------------------------------------------------------------------

`plot(sizes, norm_x=100, norm_y=100, color=None, label=None, value=None, ax=None, pad=False, bar_kwargs=None, text_kwargs=None, **kwargs)`
:   Plotting with Matplotlib.

**Parameters**

    sizes
        input for squarify
    norm_x, norm_y
        x and y values for normalization
    color
        color string or list-like (see Matplotlib documentation for details)
    label
        list-like used as label text
    value
        list-like used as value text (in most cases identical with sizes argument)
    ax
        Matplotlib Axes instance
    pad
        draw rectangles with a small gap between them
    bar_kwargs : dict
        keyword arguments passed to matplotlib.Axes.bar
    text_kwargs : dict
        keyword arguments passed to matplotlib.Axes.text
    **kwargs
        Any additional kwargs are merged into `bar_kwargs`. Explicitly provided
        kwargs here will take precedence.

**Returns**

    matplotlib.axes.Axes
        Matplotlib Axes

----------------------------------------------------------------------------------------

`squarify(sizes, x, y, dx, dy)`
:   Compute treemap rectangles.

Given a set of values, computes a treemap layout in the specified geometry
using an algorithm based on Bruls, Huizing, van Wijk, "Squarified Treemaps".
See README for example usage.

**Parameters**

    sizes : list-like of numeric values
        The set of values to compute a treemap for. `sizes` must be positive
        values sorted in descending order and they should be normalized to the
        total area (i.e., `dx * dy == sum(sizes)`)
    x, y : numeric
        The coordinates of the "origin".
    dx, dy : numeric
        The full width (`dx`) and height (`dy`) of the treemap.

**Returns**

    list[dict]
        Each dict in the returned list represents a single rectangle in the
        treemap. The order corresponds to the input order.
