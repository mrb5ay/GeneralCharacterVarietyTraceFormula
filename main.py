import numpy as np
from sympy import *
from itertools import permutations

from triangle import Triangle, Edge, Vertex

import triangulation as t

t.construct_triangulation()

t.get_peripheral_curves()

t.get_trace_of_curve()