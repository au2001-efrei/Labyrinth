#!/usr/bin/env python3

import sys
import random

def input_maze_size():
    """
    Inputs and returns two integers from the user.
    They represent the width and the height of the labyrinth, respectively.
    """

    print("Enter the size of your labyrinth:")

    width = int(input("Width: "))
    height = int(input("Height: "))
    depth = int(input("Depth: "))

    return width, height, depth

def generate_grid(width, height, depth):
    """
    Generates the initial grid for the randomized Kruskal's maze generation algorithm.
    The grid returned is a two-dimensional list of integers.
    Its first dimension is of size the height specified and its second of size the width specified.
    -1 represents walls, numbers from 0 to width * height represent open cells.
    """

    grid = []
    grid.append([[-1] * (width * 2 + 1) for y in range(height * 2 + 1)])

    for z in range(depth):
        line = []
        line.append([-1] * (width * 2 + 1))

        for y in range(height):
            column = []
            column.append(-1)

            for x in range(width):
                column.append(x + (y * width + z) * depth)
                column.append(-1)

            line.append(column)
            line.append([-1] * (width * 2 + 1))

        grid.append(line)
        grid.append([[-1] * (width * 2 + 1) for y in range(height * 2 + 1)])

    return grid

def is_maze_done(grid):
    """
    Returns True if and only if the specified grid only contains -1 and 0.
    This means the randomized Kruskal's maze generation algorithm is completed.
    """

    for line in grid:
        for column in line:
            for cell in column:
                if cell != -1 and cell != 0:
                    return False

    return True

def get_adjacent_cells(grid, x, y, z):
    """
    Returns all the adjacent valid cells to the one with the specified coordinates.
    Assumes -1 represents walls and anything else represents open cells.
    """

    adjacent = []

    for dx, dy, dz in [(-1, 0, 0), (+1, 0, 0), (0, -1, 0), (0, +1, 0), (0, 0, -1), (0, 0, +1)]:
        if z + dz < 0 or z + dz >= len(grid) or y + dy < 0 or y + dy >= len(grid[z + dz]) or x + dx < 0 or x + dx >= len(grid[z + dz][y + dy]):
            continue

        if grid[z + dz][y + dy][x + dx] == -1:
            continue

        adjacent.append((x + dx, y + dy, z + dz))

    return adjacent

def propagate(grid, x, y, z):
    """
    If the cell at the specified coordinates is a wall next to an open cell, replaces it with an open cell of the same value.
    Then, merges all the neighboring sets into the smallest one recursively.
    """

    if z < 0 or z >= len(grid) or y < 0 or y >= len(grid[z]) or x < 0 or x >= len(grid[z][y]):
        return

    minimum = None
    adjacent = get_adjacent_cells(grid, x, y, z)

    for cell in adjacent:
        if minimum is None or grid[cell[2]][cell[1]][cell[0]] < minimum:
            minimum = grid[cell[2]][cell[1]][cell[0]]

    if minimum is None:
        return

    grid[z][y][x] = minimum

    for cell in adjacent:
        if grid[cell[2]][cell[1]][cell[0]] > minimum:
            propagate(grid, cell[0], cell[1], cell[2])

def generate_maze(width, height, depth):
    """
    Generates a maze of the specified size using a derived and randomized form of Kruskal's maze generation algorithm.
    The grid returned is a two-dimensional list of integers.
    Its first dimension is of size the height specified and its second of size the width specified.
    -1 represents walls, spaces (" ") represent open cells.
    """

    grid = generate_grid(width, height, depth)
    while not is_maze_done(grid):
        orientation = random.randint(0, 2)
        if orientation == 0:
            # Vertical
            x, y, z = random.randrange(1, width) * 2, random.randrange(height) * 2 + 1, random.randrange(depth) * 2 + 1
            if grid[z][y][x] != -1 or grid[z][y][x - 1] == grid[z][y][x + 1]:
                continue
        elif orientation == 1:
            # Horizontal
            x, y, z = random.randrange(width) * 2 + 1, random.randrange(1, height) * 2, random.randrange(depth) * 2 + 1
            if grid[z][y][x] != -1 or grid[z][y - 1][x] == grid[z][y + 1][x]:
                continue
        elif orientation == 2:
            # Upsidedown
            x, y, z = random.randrange(width) * 2 + 1, random.randrange(height) * 2 + 1, random.randrange(1, depth) * 2
            if grid[z][y][x] != -1 or grid[z - 1][y][x] == grid[z + 1][y][x]:
                continue

        if grid[z][y][x] != -1:
            continue
        propagate(grid, x, y, z)

    for z in range(1, depth * 2):
        for y in range(1, height * 2):
            for x in range(1, width * 2):
                if grid[z][y][x] == 0:
                    grid[z][y][x] = " "
    return grid

def display_maze(grid):
    """
    Displays the specified maze.
    Cells with -1 are replaced with stars ("*").
    Numbers above 9 are replaced with letters, or plus ("+") if they are above 61.
    """

    first = True
    characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+"
    for z, line in enumerate(grid):
        if not first:
            print()
            print("-" * (len(line[0]) * 2 - 1))
        else:
            first = False

        print()
        print("Level", z)
        for y, column in enumerate(line):
            for x, cell in enumerate(column):
                if cell == -1:
                    print("*", end=" ")
                else:
                    if type(cell) is int:
                        cell = characters[min(cell, len(characters) - 1)]
                    elif cell == " ":
                        if z > 0 and z < len(grid) - 1 and grid[z - 1][y][x] != -1 and grid[z + 1][y][x] != -1:
                            cell = "⇕"
                        elif z > 0 and grid[z - 1][y][x] != -1:
                            cell = "⇑"
                        elif z < len(grid) - 1 and grid[z + 1][y][x] != -1:
                            cell = "⇓"
                    print(cell, end=" ")
            print()
    print()

def input_points(grid):
    """
    Inputs and returns four integers from the user.
    The first two represent the x and y coordinates of the labyrinth's entrance respectively.
    The last two represent the x and y coordinates of the labyrinth's exit respectively.
    """

    valid = False
    while not valid:
        print("Enter the coordinates of the starting point (A):")
        xA = int(input("X: "))
        yA = int(input("Y: "))
        zA = int(input("Z: "))

        valid = len(get_adjacent_cells(grid, xA, yA, zA)) == 1
        if not valid:
            print("The starting point (A) must be an external wall adjacent to an empty cell.")

    valid = False
    while not valid:
        print("Enter the coordinates of the ending point (B):")
        xB = int(input("X: "))
        yB = int(input("Y: "))
        zB = int(input("Z: "))

        valid = len(get_adjacent_cells(grid, xB, yB, zB)) == 1 and (xB != xA or yB != yA or zB != zA)
        if not valid:
            print("The ending point (B) must be an external wall adjacent to an empty cell and different from the starting point.")

    return xA, yA, zA, xB, yB, zB

def get_path(grid, distances, x, y, z):
    """
    Traces back the path from the specified coordinates to the point of distance 0.
    Returns the grid specified, replacing spaces (" ") with dots (".") along the path.
    WARNING: The distances should only describe one path of decrementing integers from the specified coordinates.
             Otherwise, the behavior is undefined and the function may return None.
    """

    solution = [[column.copy() for column in line] for line in grid]

    d = distances[z][y][x]
    while d > 0:
        for cell in get_adjacent_cells(distances, x, y, z):
            if distances[cell[2]][cell[1]][cell[0]] == d - 1:
                x, y, z = cell
                d -= 1
                break
        else:
            return None

        if solution[cell[2]][cell[1]][cell[0]] == " ":
            solution[cell[2]][cell[1]][cell[0]] = "."

    return solution

def solve_maze(grid, xA, yA, zA, xB, yB, zB):
    """
    Finds the optimal solution of the specified maze grid, where the starting point is (xA, yA) and the exit has coordinates (xB, yB).
    Returns the number of cells explored by the algorithm, the length of the shortest path, as well as the path itself.
    Assumes -1 represents walls and anything else represents open cells.
    The returned grid contains dots (".") along the path.
    """

    distances = [[[-1] * len(column) for column in line] for line in grid]

    explored = 0
    pending = [(xA, yA, zA, 0)]
    while pending:
        x, y, z, d = pending.pop(0)
        if distances[z][y][x] != -1 and distances[z][y][x] <= d:
            continue
        distances[z][y][x] = d
        explored += 1

        for cell in get_adjacent_cells(grid, x, y, z):
            pending.append((cell[0], cell[1], cell[2], d + 1))

    return explored, distances[zB][yB][xB], get_path(grid, distances, xB, yB, zB)

def main():
    """
    Executes the labyrinth program.
    """

    sys.setrecursionlimit(100000)

    width, height, depth = input_maze_size()
    grid = generate_maze(width, height, depth)

    print("Here is the random labyrinth:")
    display_maze(grid)

    xA, yA, zA, xB, yB, zB = input_points(grid)

    grid[zA][yA][xA] = "A"
    grid[zB][yB][xB] = "B"

    explored, length, solution = solve_maze(grid, xA, yA, zA, xB, yB, zB)

    if solution is not None:
        print("Here is the shortest path:")
        display_maze(solution)
        print("Number of explored cells to find the path:", explored)
        print("Length of the shortest path:", length)
    else:
        print("No solution found to the maze.")

if __name__ == "__main__":
    main()
