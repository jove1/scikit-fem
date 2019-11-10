from skfem import *
from skfem.models.poisson import laplace

from math import ceil

import numpy as np

mesh_inlet_n = 2**5
height = 1.
length = 10.
peclet = 1e2

mesh = (MeshLine(np.linspace(0, length, ceil(mesh_inlet_n / height * length)))
        * MeshLine(np.linspace(0, height / 2, mesh_inlet_n)))._splitquads()
basis = InteriorBasis(mesh, ElementTriP2())


@bilinear_form
def advection(u, du, v, dv, w):
    _, y = w.x
    velocity_0 = 6 * y * (height - y)  # parabolic plane Poiseuille
    return v * velocity_0 * du[0]


dofs = basis.get_dofs({'inlet': lambda x: x[0] == 0.,
                       'floor': lambda x: x[1] == 0.})
interior = basis.complement_dofs(dofs)

A = asm(laplace, basis) + peclet * asm(advection, basis)
t = np.zeros(basis.N)
t[dofs['floor'].all()] = 1.
t = solve(*condense(A, np.zeros_like(t), t, I=interior))


if __name__ == '__main__':

    from pathlib import Path

    mesh.plot(t[basis.nodal_dofs.flatten()], edgecolors='none')
    mesh.savefig(Path(__file__).with_suffix('.png'),
                 bbox_inches='tight', pad_inches=0)
