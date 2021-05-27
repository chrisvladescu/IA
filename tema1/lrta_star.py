"""
    Vladescu Cristiana Veronica, 342 C4
    Tema 1 - Inteligenta artificiala
"""
from constants import VALID
from math import sqrt
import pickle

source = None
destination = None
positions = None
edges = None
U_ = float('inf')
total_cost = []


def lrta_helper(source, destination):

    H = [None for pos in range(len(positions))]
    cost = 0
    path = [source]
    copy_path = []
    # Determinarea caii, pana cand aceasta se stabilizeaza
    while path != copy_path:
        # Folosirea pickle duce la reducerea timpului de executie, comparativ cu deepcopy
        copy_path = pickle.loads(pickle.dumps(path))
        cost, new_path = lrta_star(H, source, destination, [source])
        path = new_path

    cost = compute_cost(path)
    return cost, path


def lrta_star(H, state, destination, path):
    # Verific daca nodul este descoperit
    if H[state] is None:
        H[state] = get_distance(state, destination)

    min_value = float("inf")

    while state != destination and state is not None:
        # Obtin vecinii nodului
        next_states = expand(state)
        min_value = float("inf")
        next_id = None
        # Extrag cel mai profitabil vecin(costul cel mai mic)
        for connection in next_states:
            if H[connection["id"]] is None:
                computed_cost = get_distance(connection["id"], destination)
            else:
                computed_cost = H[connection["id"]] + connection["cost"]
            if computed_cost <= min_value:
                min_value = computed_cost
                next_id = connection["id"]
        # Ii setez costul si il adaug la cale
        H[state] = min_value
        path.append(next_id)

        state = next_id

    return H[destination], path


"""
    Functii auxiliare:
    => testare daca starea in care a ajuns este stare finala
    => testare daca pozitia este  valida
    => intoarce valoarea costului dintre doua stari
"""


def is_final(state):
    global destination
    return state == destination


def is_valid(id):
    global positions
    return int(positions[id]["type"]) == VALID


def get_edge_cost(starting, next):
    global edges

    for connections in edges[starting]:
        if connections["id"] == next:
            return connections["cost"]


"""
    Euristica ca intoarce valoarea distantei euclidiene. 
"""


def get_distance(id1, id2):
    x = positions[id1]["x"] - positions[id2]["x"]
    y = positions[id1]["y"] - positions[id2]["y"]
    return int(sqrt(pow(x, 2) + pow(y, 2)))


"""
    Expandarea starii curente: se intorc toti veciniii ce nu sunt obstacole
"""


def expand(state):
    global edges
    next_states = []

    for connection in edges[state]:
        if is_valid(connection["id"]) is True:
            next_states.append(connection)
    return next_states


"""
    Calcularea costului caii obtinute
"""


def compute_cost(path):
    cost = 0

    copy_path = pickle.loads(pickle.dumps(path))
    starting_state = copy_path.pop()

    while copy_path != []:
        next_state = copy_path.pop()
        cost += get_edge_cost(starting_state, next_state)
        starting_state = next_state

    return cost


def main(s, d, pos, e):
    global source
    global destination
    global positions
    global edges

    source = s
    destination = d
    positions = pos
    edges = e
    return lrta_helper(source, destination)
