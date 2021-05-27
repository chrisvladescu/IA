"""
    Vladescu Cristiana Veronica, 342 C4
    Tema 1 - Inteligenta artificiala
"""
import matplotlib.pyplot as pyplot
import matplotlib.colors as colors
from constants import OBSTACLE

"""
    Realizarea hartii care sa prezinte grafic calea obtinuta.
    Pozitiile sunt colorate in functie de tipul acestora:
    => daca este pozitie de star : cornflowerblue
    => daca este pozitie de final: midnight blue
    => daca face parte din cale: sandybrown
    => daca este obstacol: firebrick
"""


def main(N, positions, source, destination, path):
    map_colors = colors.ListedColormap(
        ["papayawhip", "firebrick", "cornflowerblue", "midnightblue", "sandybrown"])
    values = [0, 1, 2, 3, 4, 5]
    boundary_norm = colors.BoundaryNorm(values, map_colors.N)

    map_image = [[0 for col in range(N + 1)] for row in range(N+1)]

    for pos_id in range(1, len(positions)):
        pos = positions[pos_id]
        if pos["type"] == OBSTACLE:
            map_image[pos["x"]][pos["y"]] = 1
        elif pos_id == source:
            map_image[pos["x"]][pos["y"]] = 2
        elif pos_id == destination:
            map_image[pos["x"]][pos["y"]] = 3
        elif pos_id in path and pos_id != source and pos_id != destination:
            map_image[pos["x"]][pos["y"]] = 4

    pyplot.imshow(map_image, map_colors, boundary_norm,
                  interpolation='nearest')


if __name__ == "__main__":
    main(0, [], None, None, [])
