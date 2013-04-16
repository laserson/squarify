squaripy
========

Pure Python implementation of squarify treemap layout algorithm.

Based on algorithm from Bruls, Huizing, van Wijk, "Squarified Treemaps", but
implements it differently.


Installation
------------

Using pip:

    pip install squaripy

or using the source:

    git clone git://github.com/laserson/squaripy.git
    cd squarify
    python setup.py install

The last step may require `sudo` if you don't have root access.


Usage (by example)
------------------

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
values = squaripy.normalize_sizes(values, width, height)

# returns a list of rectangles
rects = squaripy.squarify(values, x, y, width, height)
```

The main function is `squarify` (note the "f" instead of "p").

Given a list of sizes in descending order, `squarify` will return a list of JSON
objects that represent rectangles in a treemap layout.
