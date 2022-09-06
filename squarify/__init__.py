# Squarified Treemap Layout
# Implements algorithm from Bruls, Huizing, van Wijk, "Squarified Treemaps"
#   (but not using their pseudocode)


# INTERNAL FUNCTIONS not meant to be used by the user

import re

_location_error_message = "Invalid location string: '%s'."


def pad_rectangle(rect):
    if rect["dx"] > 2:
        rect["x"] += 1
        rect["dx"] -= 2
    if rect["dy"] > 2:
        rect["y"] += 1
        rect["dy"] -= 2


def layoutrow(sizes, x, y, dx, dy):
    # generate rects for each size in sizes
    # dx >= dy
    # they will fill up height dy, and width will be determined by their area
    # sizes should be pre-normalized wrt dx * dy (i.e., they should be same units)
    covered_area = sum(sizes)
    width = covered_area / dy
    rects = []
    for size in sizes:
        rects.append({"x": x, "y": y, "dx": width, "dy": size / width})
        y += size / width
    return rects


def layoutcol(sizes, x, y, dx, dy):
    # generate rects for each size in sizes
    # dx < dy
    # they will fill up width dx, and height will be determined by their area
    # sizes should be pre-normalized wrt dx * dy (i.e., they should be same units)
    covered_area = sum(sizes)
    height = covered_area / dx
    rects = []
    for size in sizes:
        rects.append({"x": x, "y": y, "dx": size / height, "dy": height})
        x += size / height
    return rects


def layout(sizes, x, y, dx, dy):
    return (
        layoutrow(sizes, x, y, dx, dy) if dx >= dy else layoutcol(sizes, x, y, dx, dy)
    )


def leftoverrow(sizes, x, y, dx, dy):
    # compute remaining area when dx >= dy
    covered_area = sum(sizes)
    width = covered_area / dy
    leftover_x = x + width
    leftover_y = y
    leftover_dx = dx - width
    leftover_dy = dy
    return (leftover_x, leftover_y, leftover_dx, leftover_dy)


def leftovercol(sizes, x, y, dx, dy):
    # compute remaining area when dx >= dy
    covered_area = sum(sizes)
    height = covered_area / dx
    leftover_x = x
    leftover_y = y + height
    leftover_dx = dx
    leftover_dy = dy - height
    return (leftover_x, leftover_y, leftover_dx, leftover_dy)


def leftover(sizes, x, y, dx, dy):
    return (
        leftoverrow(sizes, x, y, dx, dy)
        if dx >= dy
        else leftovercol(sizes, x, y, dx, dy)
    )


def worst_ratio(sizes, x, y, dx, dy):
    return max(
        [
            max(rect["dx"] / rect["dy"], rect["dy"] / rect["dx"])
            for rect in layout(sizes, x, y, dx, dy)
        ]
    )


# PUBLIC API


def squarify(sizes, x, y, dx, dy):
    """Compute treemap rectangles.

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
    """
    sizes = list(map(float, sizes))

    if len(sizes) == 0:
        return []

    if len(sizes) == 1:
        return layout(sizes, x, y, dx, dy)

    # figure out where 'split' should be
    i = 1
    while i < len(sizes) and worst_ratio(sizes[:i], x, y, dx, dy) >= worst_ratio(
        sizes[: (i + 1)], x, y, dx, dy
    ):
        i += 1
    current = sizes[:i]
    remaining = sizes[i:]

    (leftover_x, leftover_y, leftover_dx, leftover_dy) = leftover(current, x, y, dx, dy)
    return layout(current, x, y, dx, dy) + squarify(
        remaining, leftover_x, leftover_y, leftover_dx, leftover_dy
    )


def padded_squarify(sizes, x, y, dx, dy):
    """Compute padded treemap rectangles.

    See `squarify` docstring for details. The only difference is that the
    returned rectangles have been "padded" to allow for a visible border.
    """
    rects = squarify(sizes, x, y, dx, dy)
    for rect in rects:
        pad_rectangle(rect)
    return rects


def normalize_sizes(sizes, dx, dy):
    """Normalize list of values.

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
    """
    total_size = sum(sizes)
    total_area = dx * dy
    sizes = map(float, sizes)
    sizes = map(lambda size: size * total_area / total_size, sizes)
    return list(sizes)


# helpers for annot placement
_v_offsets = {
    "top": lambda dy: dy - 1,
    "center": lambda dy: dy / 2,
    "bottom": lambda dy: 1,
}
_h_offsets = {
    "left": lambda dx: 1,
    "center": lambda dx: dx / 2,
    "right": lambda dx: dx - 1,
}


def plot(
    sizes,
    norm_x=100,
    norm_y=100,
    color=None,
    label=None,
    value=None,
    loc=None,
    ax=None,
    pad=False,
    bar_kwargs=None,
    text_kwargs=None,
    **kwargs,
):
    """Plotting with Matplotlib.

    Parameters
    ----------
    sizes :
        input for squarify

    norm_x, norm_y :
        x and y values for normalization

    color :
        color string or list-like (see Matplotlib documentation for details)

    label :
        list-like used as label text

    value :
        list-like used as value text (in most cases identical with sizes argument)

    loc :
        The location of the texts (labels and/or values) inside the rectangles.

        The strings
        ``'top left', 'top right', 'bottom left', 'bottom right'``
        place the text at the corresponding corner of the rectangles.

        The strings
        ``'top center', 'bottom center', 'center left', 'center right'``
        place the text at the center of the corresponding edge of the
        rectangles.

        The string ``'center'`` places the text at the center of the rectangles.

        ``NoneType`` defaults to ``'center'``.

    ax :
        Matplotlib Axes instance

    pad :
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
    """

    import matplotlib.pyplot as plt

    if ax is None:
        ax = plt.gca()

    if color is None:
        import matplotlib.cm
        import random

        cmap = matplotlib.cm.get_cmap()
        color = [cmap(random.random()) for i in range(len(sizes))]

    if bar_kwargs is None:
        bar_kwargs = {}
    if text_kwargs is None:
        text_kwargs = {}
    if len(kwargs) > 0:
        bar_kwargs.update(kwargs)

    normed = normalize_sizes(sizes, norm_x, norm_y)

    if pad:
        rects = padded_squarify(normed, 0, 0, norm_x, norm_y)
    else:
        rects = squarify(normed, 0, 0, norm_x, norm_y)

    x = [rect["x"] for rect in rects]
    y = [rect["y"] for rect in rects]
    dx = [rect["dx"] for rect in rects]
    dy = [rect["dy"] for rect in rects]

    ax.bar(
        x, dy, width=dx, bottom=y, color=color, label=label, align="edge", **bar_kwargs
    )

    if value and label:
        # If both values and labels are specified, unify them in single text fields
        texts = ["%s\n%s" % (l, v) for l, v in zip(label, value)]
    elif value or label:
        # Otherwise keep only the non-empty one as text fields
        texts = value if value else label
    else:
        texts = None

    if texts:
        # Set up annot locations
        if loc is None or loc == "center":
            va, ha = "center", "center"
        else:
            va, ha = loc.split()
            if va not in {"top", "center", "bottom"}:
                raise ValueError(f"Invalid `loc` string: {loc}")
            if ha not in {"left", "center", "right"}:
                raise ValueError(f"Invalid `loc` string: {loc}")

        # Add the annot
        for text, rect in zip(texts, rects):
            x, y, dx, dy = rect["x"], rect["y"], rect["dx"], rect["dy"]
            ax.text(
                x + _h_offsets[ha](dx),
                y + _v_offsets[va](dy),
                text,
                va=va,
                ha=ha,
                **text_kwargs,
            )

    ax.set_xlim(0, norm_x)
    ax.set_ylim(0, norm_y)

    return ax
