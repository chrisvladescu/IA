"""
    Vladescu Cristiana Veronica, 342 C4
    Tema 1 - Inteligenta artificiala
"""
from constants import VALID
from math import sqrt
from heapq import heappush, heappop
import pickle

source = None
destination = None
positions = None
edges = None

U_ = float('inf')
total_cost = []


def branch_and_bound(source, destination, positions, edges):
    frontier = []
    heappush(frontier, (0 + heuristic(source, destination), source))
    # Nodurile descoperite ca dicționar nod -> (părinte, cost-până-la-nod)
    discovered = {source: [None, 0]}
    while frontier:
        # Extrag nodul n cu distanta minima cu heappop
        n = heappop(frontier)
        pos_n = n[1]
        # Verific daca nodul este final
        if is_final(pos_n) is True:
            break
        # Extrag vecinii nodului
        neighbours_n = expand(pos_n)

        # Verific pentru fiecare dintre vecini costul si ii adaug in frontiera
        # doar pe cei nedescoperiti
        for neighbour in neighbours_n:
            cost = discovered.get(pos_n)[1] + 1
            if neighbour["id"] in discovered:
                if cost < discovered[neighbour["id"]][1]:
                    discovered[neighbour["id"]][1] = cost
            else:
                discovered[neighbour["id"]] = [pos_n, cost]
                cost += heuristic(neighbour["id"], destination)
                heappush(frontier, (cost, neighbour["id"]))

    path = []
    node = destination

    while node != None:
        path.append(node)
        node = discovered[node][0]

    path.reverse()

    cost = compute_cost(path)

    return cost, path


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
    return int(positions[id]["type"]) == VALID


def get_edge_cost(starting, next):
    global edges

    for connections in edges[starting]:
        if connections["id"] == next:
            return connections["cost"]


"""
    Euristica ca intoarce valoarea distantei euclidiene. 
"""


def heuristic(id1, id2):
    x = positions[id1]["x"] - positions[id2]["x"]
    y = positions[id1]["y"] - positions[id2]["y"]
    return int(sqrt(pow(x, 2) + pow(y, 2)))


"""
    Expandarea starii curente: se intorc toti veciniii ce nu sunt obstacole
"""


def expand(state):
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
    return branch_and_bound(s, d, pos, e)
