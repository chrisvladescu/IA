"""
    Vladescu Cristiana Veronica, 342 C4
    Tema 1 - Inteligenta artificiala
"""
from constants import VALID, OBSTACLE
import pickle
from math import sqrt

source = None
destination = None
positions = None
edges = None
U_ = float('inf')
total_cost = []


def heuristic(source, cost):
    global U_
    global total_cost

    U_ = 0
    best_path = []
    path = [source]

    while best_path == [] and U_ != float('inf'):
        # Reinitializez in fiecare iteratie vectorul de costuri, dar si variabilele
        visited = {}
        U = U_
        U_ = float('inf')
        total_cost = [-1 for x in range(len(positions) + 1)]
        total_cost[source] = 0
        best_path = run_heuristic(source, 0, U, path, visited)
    return best_path


def run_heuristic(state, cost, U, path, visited):
    global U_
    global total_cost
    p = []
    # Marchez starea ca vizitata
    visited[state] = cost
    # Verific daca starea este finala
    if (is_final(state)):
        return cost, path

    # Determin vecinii starii
    next_states = expand(state)

    for connection in next_states:
        heuristic_cost = get_distance(state, connection["id"])
        final_cost = cost + connection["cost"] + heuristic_cost
        # Verific pentru care dintre vecini are rost sa continui expansiunea:
        # Daca vecinul nu a fost vizitat sau daca acum se inregistreaza un cost
        # mai mic decat cel deja obtinut, atunci voi continua cautarea si din acesta
        if connection["id"] not in visited.keys() or visited[connection["id"]] > final_cost:
            if final_cost <= U:
                if total_cost[connection["id"]] == -1 or final_cost <= total_cost[connection["id"]]:
                    copy_path = pickle.loads(pickle.dumps(path))
                    copy_path.append(connection["id"])
                    total_cost[connection["id"]] = final_cost
                    p += run_heuristic(connection["id"], final_cost - heuristic_cost,
                                       U, copy_path, visited)
                    if p != []:
                        return p
            # Actualizez limita de cost
            elif final_cost < U_:
                U_ = final_cost
    return []


"""
    Functii auxiliare:
    => testare daca starea in care a ajuns este stare finala
    => testare daca pozitia este  valida
"""


def is_final(state):
    global destination
    return state == destination


def is_valid(id):
    return int(positions[id]["type"]) == VALID


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
    Euristica ca intoarce valoarea distantei pe diagonala. 
"""


def get_distance(id1, id2):
    D = 1
    D_2 = 1
    dx = abs(positions[id1]["x"] - positions[id2]["x"])
    dy = abs(positions[id1]["y"] - positions[id2]["y"])
    return D*dx + (D_2 - 2 * D) * min(dx, dy)


def main(s, d, pos, e):
    global source
    global destination
    global positions
    global edges

    source = s
    destination = d
    positions = pos
    edges = e
    return heuristic(source, 0)
