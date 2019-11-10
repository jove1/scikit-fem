import numpy as np
from ..element_h1 import ElementH1


class ElementTriP0(ElementH1):
    interior_dofs = 1
    dim = 2
    maxdeg = 0
    dofnames = ['u']
    doflocs = np.array([[.5, .5]])

    def lbasis(self, X, i):
        return 1 + 0*X[0, :], 0*X
