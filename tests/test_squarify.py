from squarify import normalize_sizes, squarify


expected = [
    {"dy": 433, "dx": 327.7153558052434, "x": 0, "y": 0},
    {"dy": 330.0862676056338, "dx": 372.2846441947566, "x": 327.7153558052434, "y": 0},
    {
        "dy": 102.9137323943662,
        "dx": 215.0977944236371,
        "x": 327.7153558052434,
        "y": 330.0862676056338,
    },
    {
        "dy": 102.9137323943662,
        "dx": 68.94160077680677,
        "x": 542.8131502288805,
        "y": 330.0862676056338,
    },
    {
        "dy": 80.40135343309854,
        "dx": 88.24524899431273,
        "x": 611.7547510056874,
        "y": 330.0862676056338,
    },
    {
        "dy": 22.51237896126767,
        "dx": 88.2452489943124,
        "x": 611.7547510056874,
        "y": 410.4876210387323,
    },
]


def test_squarify():
    x = 0.0
    y = 0.0
    width = 700.0
    height = 433.0
    values = [500, 433, 78, 25, 25, 7]
    values = normalize_sizes(values, width, height)
    observed = squarify(values, x, y, width, height)
    assert len(observed) == len(expected)
    for (o, e) in zip(observed, expected):
        assert len(o) == 4
        assert set(o.keys()) == set(["dx", "dy", "x", "y"])
        assert o["dx"] == e["dx"]
        assert o["dy"] == e["dy"]
        assert o["x"] == e["x"]
        assert o["y"] == e["y"]
