Module [Squarify](squarify/__init__.py)
===============

Functions
---------

    
`layout(sizes, x, y, dx, dy)`
:   

    
`layoutcol(sizes, x, y, dx, dy)`
:   

    
`layoutrow(sizes, x, y, dx, dy)`
:   

    
`leftover(sizes, x, y, dx, dy)`
:   

    
`leftovercol(sizes, x, y, dx, dy)`
:   

    
`leftoverrow(sizes, x, y, dx, dy)`
:   

    
`normalize_sizes(sizes, dx, dy)`
:   Normalize list of values.
    
    Normalizes a list of numeric values so that `sum(sizes) == dx * dy`.
    
    Parameters
    ----------
    sizes : list-like of numeric values
        Input list of numeric values to normalize.
    dx, dy : numeric
        The dimensions of the full rectangle to normalize total values to.
    
    Returns
    -------
    list[numeric]
        The normalized values.

    
`pad_rectangle(rect)`
:   

    
`padded_squarify(sizes, x, y, dx, dy)`
:   Compute padded treemap rectangles.
    
    See `squarify` docstring for details. The only difference is that the
    returned rectangles have been "padded" to allow for a visible border.

    
`plot(sizes, norm_x=100, norm_y=100, color=None, label=None, value=None, ax=None, pad=False, bar_kwargs=None, text_kwargs=None, **kwargs)`
:   Plotting with Matplotlib.
    
    Parameters
    ----------
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
    
    Returns
    -------
    matplotlib.axes.Axes
        Matplotlib Axes

    
`squarify(sizes, x, y, dx, dy)`
:   Compute treemap rectangles.
    
    Given a set of values, computes a treemap layout in the specified geometry
    using an algorithm based on Bruls, Huizing, van Wijk, "Squarified Treemaps".
    See README for example usage.
    
    Parameters
    ----------
    sizes : list-like of numeric values
        The set of values to compute a treemap for. `sizes` must be positive
        values sorted in descending order and they should be normalized to the
        total area (i.e., `dx * dy == sum(sizes)`)
    x, y : numeric
        The coordinates of the "origin".
    dx, dy : numeric
        The full width (`dx`) and height (`dy`) of the treemap.
    
    Returns
    -------
    list[dict]
        Each dict in the returned list represents a single rectangle in the
        treemap. The order corresponds to the input order.

    
`worst_ratio(sizes, x, y, dx, dy)`
:   

-----
