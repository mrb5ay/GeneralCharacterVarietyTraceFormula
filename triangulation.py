import numpy as np
from sympy import *
from itertools import permutations
import pickle

from triangle import Triangle, Edge, Vertex
from trace import trace_formula

v = []
e = []
t = []


# Construct Vertices:
# int - num_vertices specifies the number of punctures
# list[string] - vertex_names is an optional argument. by default vertices are numbered 1 to n.
def construct_vertices(num_vertices, vertex_names=None):
    for i in range(num_vertices):
        if vertex_names is not None:
            vertex = Vertex(vertex_names[i])
        else:
            vertex = Vertex(str(i + 1))
        v.append(vertex)


# Construct Edges
# int - num_edges specifies the number of edges in the triangulation
# list[(vertex1, vertex2)] - specifies the endpoints of each edge
def construct_edges(num_edges, endpoints):
    for i in range(num_edges):
        edge = Edge(endpoints[i][0], endpoints[i][1])
        e.append(edge)


# Construct Triangles
# int - num_triangles specifies the number of triangles in the triangulation
# list[(vertex1, vertex2, vertex3)] - specifies the vertices of each triangle
def construct_triangles(num_triangles, vertices):
    for i in range(num_triangles):
        triangle = Triangle([vertices[i][0], vertices[i][1], vertices[i][2]])
        t.append(triangle)


# Prints the triangulation
def print_triangulation():
    print("Vertices:", v)
    print("Edges:", e)
    print("Triangles:", t)
    print("")


# Set up for creating a triangulation
def construct_triangulation():
    with open("triangulation.txt", "rb") as f:
        check = f.read(1)
        if check:
            while True:
                print("Detected a locally saved triangulation. Would you like to load it? (Y or N).")
                use_locally_saved = input()
                if use_locally_saved == "Y":
                    load_triangulation()
                    return
                elif use_locally_saved == "N":
                    break
                else:
                    print("Please enter either 'Y' or 'N'.")

    while True:
        print("Input the number of vertices: ")
        try:
            num_vertices = int(input())
        except ValueError:
            print("Please enter a valid integer.")
        else:
            break

    while True:
        print("Would you like to name the vertices? Y or N.")
        vertices_are_named = input()
        if vertices_are_named != "Y" and vertices_are_named != "N":
            print("Enter either 'Y' or 'N'.")
        else:
            break

    vertex_names = None
    if vertices_are_named == "Y":
        print("List all vertex names in one line, separated by whitespace: ")
        vertex_names = input()
        vertex_names = vertex_names.split(" ")

    construct_vertices(num_vertices, vertex_names=vertex_names)

    while True:
        print("Input the number of edges: ")
        try:
            num_edges = int(input())
        except ValueError:
            print("Please enter a valid integer.")
        else:
            break

    endpoints = []
    for i in range(num_edges):
        while True:
            print("The vertex names are", [x.name for x in v])
            print("List the endpoints for edge", i + 1, "separated by whitespace:")
            endpoint_for_edge = input()
            endpoint_for_edge = endpoint_for_edge.split(" ")
            try:
                endpoint_for_edge[0] = [x for x in v if x.name == endpoint_for_edge[0]][0]
                endpoint_for_edge[1] = [x for x in v if x.name == endpoint_for_edge[1]][0]
            except IndexError:
                print("Could not understand those vertex names. Try again.")
            else:
                endpoints.append(endpoint_for_edge)
                break

    construct_edges(num_edges, endpoints)

    while True:
        print("Input the number of triangles: ")
        try:
            num_triangles = int(input())
        except ValueError:
            print("Please enter a valid integer.")
        else:
            break

    vertices = []
    for i in range(num_triangles):
        while True:
            print("The vertex names are", [x.name for x in v])
            print("List the vertices for triangle", i, "separated by whitespace:")
            vertices_for_triangle = input()
            vertices_for_triangle = vertices_for_triangle.split(" ")
            try:
                vertices_for_triangle[0] = [x for x in v if x.name == vertices_for_triangle[0]][0]
                vertices_for_triangle[1] = [x for x in v if x.name == vertices_for_triangle[1]][0]
                vertices_for_triangle[2] = [x for x in v if x.name == vertices_for_triangle[2]][0]
            except IndexError:
                print("Could not understand those vertex names. Try again.")
            else:
                vertices.append(vertices_for_triangle)
                break

    construct_triangles(num_triangles, vertices)

    print_triangulation()

    save_triangulation()


# Determine whether edges are adjacent or not. (and fill out whether they are right or left).
def find_left_and_right_edges():
    original_edge1 = [x for x in e if set(x.endpoints) == {t[0].v[0], t[0].v[1]}][0]
    original_edge2 = [x for x in e if set(x.endpoints) == {t[0].v[1], t[0].v[2]}][0]
    original_edge3 = [x for x in e if set(x.endpoints) == {t[0].v[0], t[0].v[2]}][0]

    original_edge1.left.append(original_edge2)
    original_edge1.right.append(original_edge3)

    original_edge2.right.append(original_edge1)
    original_edge2.left.append(original_edge3)

    original_edge3.left.append(original_edge1)
    original_edge3.right.append(original_edge2)

    triangles_to_process = [y for y in t if is_neighboring(y, t[0])]
    triangles_processed = [t[0]]
    i = 0
    while len(triangles_processed) < len(t):
        if is_neighboring(triangles_to_process[0], triangles_processed[i]):
            shared_vertices = [x for x in triangles_to_process[0].v if x in triangles_processed[i].v]
            shared_edge = [y for y in e if set(y.endpoints) == set(shared_vertices)][0]

            new_vertex = list(set(triangles_to_process[0].v) - set(shared_edge.endpoints))[0]

            shared_edge_left = shared_edge.left[0]
            shared_edge_right = shared_edge.right[0]

            new_right_edge_vertex = [z for z in shared_edge_left.endpoints if z in triangles_to_process[0].v]
            new_left_edge_vertex = [z for z in shared_edge_right.endpoints if z in triangles_to_process[0].v]

            new_right_edge_vertex.append(new_vertex)
            new_left_edge_vertex.append(new_vertex)

            new_right_edge = [w for w in e if set(w.endpoints) == set(new_right_edge_vertex)][0]
            new_left_edge = [w for w in e if set(w.endpoints) == set(new_left_edge_vertex)][0]

            shared_edge.left.append(new_left_edge)
            shared_edge.right.append(new_right_edge)

            new_left_edge.left.append(new_right_edge)
            new_left_edge.right.append(shared_edge)

            new_right_edge.left.append(shared_edge)
            new_right_edge.right.append(new_left_edge)

            triangles_processed.append(triangles_to_process[0])

            for triangle in t:
                if is_neighboring(triangles_to_process[0], triangle) and triangle not in triangles_processed\
                        and triangle not in triangles_to_process:
                    triangles_to_process.append(triangle)

            del triangles_to_process[0]
        else:
            i = i + 1


# Gets the peripheral curves for the triangulation
def get_peripheral_curves():
    find_left_and_right_edges()

    for x in v:
        incident_triangles = []
        for y in t:
            if x in y.v:
                incident_triangles.append(y)
        ordered_incident_triangles = [incident_triangles[0]]
        del incident_triangles[0]
        i = 0
        while len(incident_triangles) > 0:
            i = (i + 1) % len(incident_triangles)
            if is_neighboring(ordered_incident_triangles[-1], incident_triangles[i]):
                ordered_incident_triangles.append(incident_triangles[i])
                del incident_triangles[i]
        ordered_incident_triangles.append(ordered_incident_triangles[0])
        print("Peripheral curve about vertex", x)
        trace_formula(ordered_incident_triangles, e, matrix_representation=True)


# Returns whether two triangles share an edge (aka whether they are neighbors)
def is_neighboring(triangle1, triangle2):
    if len([x for x in triangle1.v if x in triangle2.v]) == 2:
        return True
    else:
        return False


# The following code is for saving and loading triangulations.
class Triangulation:
    def __init__(self, vertices, edges, triangles):
        self.v = vertices
        self.e = edges
        self.t = triangles


def save_triangulation():
    T = Triangulation(v, e, t)
    with open("triangulation.txt", "wb") as f:
        pickle.dump(T, f)


def load_triangulation():
    global v, e, t
    with open("triangulation.txt", "rb") as f:
        T = pickle.load(f)
    v = T.v
    e = T.e
    t = T.t
    print("Loaded triangulation: ")
    print_triangulation()


def get_trace_of_curve():
    curve_path = []
    triangle_names = [x.v[0].name + x.v[1].name + x.v[2].name for x in t]
    print("Input the first triangle intersected by the simple closed curve.")
    while True:
        print("The triangles are", triangle_names)
        triangle_input = input()
        if triangle_input in triangle_names:
            triangle = [x for x in t if x.v[0].name + x.v[1].name + x.v[2].name == triangle_input][0]
            curve_path.append(triangle)
            if triangle == curve_path[0] and len(curve_path) > 1:
                print("Simple closed curve completed with path", curve_path)
                break
            print("Input the next triangle intersected by the simple closed curve.")
        else:
            print("Enter the triangle name as listed above.")

    trace_formula(curve_path, e)


