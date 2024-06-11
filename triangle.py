import numpy as np
from sympy import *


class Vertex:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "v_" + self.name

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other_vertex):
        return self.name == other_vertex.name

    def __hash__(self):
        return hash(self.name)


class Edge:
    def __init__(self, v_1, v_2, lambda_length=None):
        if lambda_length is None:
            self.length = symbols("e_" + v_1.name + v_2.name, positive=True, real=True)
        else:
            self.length = lambda_length
        self.endpoints = [v_1, v_2]
        self.left = []
        self.right = []

    def __str__(self):
        return "e_" + self.endpoints[0].name + self.endpoints[1].name

    def __eq__(self, other_edge):
        return set(self.endpoints) == set(other_edge.endpoints)

    def __repr__(self):
        return self.__str__()


class Triangle:
    def __init__(self, v, epsilon=1):
        self.sign = epsilon
        self.v = v

    def switchSign(self):
        return Triangle(self.v, epsilon=-1*self.sign)

    def __str__(self):
        return "T_" + self.v[0].name + self.v[1].name + self.v[2].name

    def __repr__(self):
        return "T_" + self.v[0].name + self.v[1].name + self.v[2].name

    def __eq__(self, other_triangle):
        return set(self.v) == set(other_triangle.v)

