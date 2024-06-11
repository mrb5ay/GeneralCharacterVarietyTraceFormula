import numpy as np
from sympy import *
from itertools import permutations

from triangle import Triangle, Edge, Vertex


# Takes in the triangles which the curve travels through (in order)
# The same triangle should be listed at the beginning and end
# Takes in the vertices, edges, and triangles of the triangulation.
# Returns the trace of the curve.
def trace_formula(triangles, e, verbose=False,  matrix_representation=False):
    # Get the list of edges which the s.c.c intersects
    edge_list = []
    for i in range(len(triangles) - 1):
        next_edge = (set(triangles[i].v) & set(triangles[i + 1].v))
        next_edge = [x for x in e if set(x.endpoints) == next_edge][0]
        edge_list.append(next_edge)
    if verbose:
        print("")
        print("Edges Crossed: ", edge_list)
        print("")
    # Get the matrices for the formula
    matrix_list = []
    edge_product = 1
    for j in range(len(edge_list)):
        edge_product = edge_product * edge_list[j].length
        k = (j + 1) % len(edge_list)
        # Get the third edge (which the curve does not intersect) of the triangle
        other_edge = set(edge_list[j].endpoints).symmetric_difference(set(edge_list[k].endpoints))
        other_edge = [x for x in e if set(x.endpoints) == other_edge][0]

        # If it makes a left-hand turn:
        if edge_list[k] in edge_list[j].left:
            matrix_list.append(
                Matrix([[edge_list[j].length, triangles[k].sign * other_edge.length], [0, edge_list[k].length]]))
        # If it makes a right-hand turn:
        elif edge_list[k] in edge_list[j].right:
            matrix_list.append(
                Matrix([[edge_list[k].length, 0], [triangles[k].sign * other_edge.length, edge_list[j].length]]))
        # If something was wrong with the given s.c.c. path:
        else:
            print("Error. Edge ", edge_list[k], " is not adjacent to edge ", edge_list[j])
    if verbose:
        print("")
        print("Matrices in Product: ", matrix_list)
        print("")
    matrix_representation = Matrix([[1, 0], [0, 1]])
    for m in matrix_list:
        matrix_representation = matrix_representation * m
    matrix_representation = expand(matrix_representation / edge_product)

    if matrix_representation:
        print("")
        print("Resulting  matrix is")
        print("")
        print(matrix_representation)
    print("")
    print("Trace: ")
    print(Trace(matrix_representation).simplify())
    print("")
