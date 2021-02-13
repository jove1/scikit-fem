"""Drawing meshes using svg."""

from functools import singledispatch

import numpy as np

from ..mesh import Mesh2D
from ..assembly import InteriorBasis


@singledispatch
def draw(m, **kwargs) -> str:
    """Visualise meshes by drawing the edges.

    Parameters
    ----------
    m
        A mesh object.

    Returns
    -------
    string
        The svg xml source as a string.

    """
    raise NotImplementedError("Type {} not supported.".format(type(m)))


@draw.register(Mesh2D)
def draw_mesh2d(m: Mesh2D, **kwargs) -> str:
    """Support for two-dimensional meshes."""
    if "boundaries_only" in kwargs:
        facets = m.facets[:, m.boundary_facets()]
    else:
        facets = m.facets
    p = m.p
    maxx = np.max(p[0])
    minx = np.min(p[0])
    maxy = np.max(p[1])
    miny = np.min(p[1])
    width = kwargs["width"] if "width" in kwargs else 300
    if "height" in kwargs:
        height = kwargs["height"]
    else:
        height = width * (maxy - miny) / (maxx - miny)
    stroke = kwargs["stroke"] if "stroke" in kwargs else 1
    sx = (width - 2 * stroke) / (maxx - minx)
    sy = (height - 2 * stroke) / (maxy - miny)
    p[0] = sx * (p[0] - miny) + stroke
    p[1] = sy * (maxy - p[1]) + stroke
    template = ("""<line x1="{}" y1="{}" x2="{}" y2="{}" """
                """style="stroke:black;stroke-width:{}"/>""")
    lines = ""
    for s, t, u, v in zip(p[0, facets[0]],
                          p[1, facets[0]],
                          p[0, facets[1]],
                          p[1, facets[1]]):
        lines += template.format(s, t, u, v, stroke)
    return ("""<svg xmlns="http://www.w3.org/2000/svg" version="1.1" """
            """width="{}" height="{}">{}</svg>""").format(width, height, lines)


@draw.register(InteriorBasis)
def draw_basis(ib: InteriorBasis, **kwargs) -> str:
    Nrefs = kwargs["Nrefs"] if "Nrefs" in kwargs else 2
    m, _ = ib.refinterp(ib.mesh.p[0], Nrefs=Nrefs)
    return draw(m, boundaries_only=True, **kwargs)
