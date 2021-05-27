"""
    Vladescu Cristiana Veronica, 342 C4
    Tema 1 - Inteligenta artificiala
"""
from constants import VALID, OBSTACLE, INPUTS
from dfid import main as dfid
from ida_star import main as ida_star
from lrta_star import main as lrta_star
from heuristic import main as heuristic
from branch_and_bound import main as branch_and_bound
from draw_map import main as print_map

import time


def main():

    source, destination, N, positions, edges = init_env(INPUTS[1])
    start = time.time()
    cost, path = ida_star(source, destination, positions, edges)
    end = time.time()
    print(f"Cost: {cost}")
    print(f"Path: {path}")
    print(f"Time: {end - start}")
    print_map(N, positions, source, destination, path)


def init_env(filename):
    source = None
    destination = None
    source_id = 0
    destination_id = 0
    positions = []
    edges = []

    with open(filename) as input_file:
        N = 0
        mouse_info = input_file.readline()
        cheese_info = input_file.readline()
        source = get_coordinates(mouse_info)
        destination = get_coordinates(cheese_info)

        positions_no = int(input_file.readline())

        # Salvez pozitiile intr-o lista, unde indexul elementului
        # corespunde cu id-ul pozitiei.
        positions = [[] for pos in range(positions_no + 1)]
        for _ in range(positions_no):
            pos_info = input_file.readline()
            pos_id, x, y, pos_type = get_position(pos_info)
            N = max(N, x, y)
            positions[pos_id] = {"x": x, "y": y, "type": pos_type}

        edges_no = int(input_file.readline())

        # Salvez conexiunile intr-o matrice, adaugand pentru fiecare nod cate
        # o conexiune in lista proprie catre celalat nod.
        edges = [[] for pos in range(positions_no + 1)]
        for _ in range(edges_no):
            edge_info = input_file.readline()
            pos_id1, pos_id2, cost = get_edge(edge_info)
            edges[pos_id1].append({"id": pos_id2, "cost": cost})
            edges[pos_id2].append({"id": pos_id1, "cost": cost})

        for no in range(1, positions_no+1):
            pos = positions[no]
            if pos["x"] == source[0] and pos["y"] == source[1]:
                source_id = positions.index(pos)
            if pos["x"] == destination[0] and pos["y"] == destination[1]:
                destination_id = positions.index(pos)

    return source_id, destination_id, N, positions, edges


"""
    Functii de extragere a informatiilor din fisierul de input.
"""


def get_coordinates(information):
    x = int(information.split(",")[0])
    y = int(information.split(",")[1])
    return [x, y]


def get_position(information):
    data = information.split(",")
    pos_id = int(data[0])
    pos_x = int(data[1])
    pos_y = int(data[2])
    pos_type = VALID
    if len(data) == 4:
        pos_type = OBSTACLE
    return pos_id, pos_x, pos_y, pos_type


def get_edge(information):
    pos_id1 = int(information.split(",")[0])
    pos_id2 = int(information.split(",")[1])
    edge_cost = int(information.split(",")[2])
    return pos_id1, pos_id2, edge_cost


if __name__ == "__main__":
    main()
