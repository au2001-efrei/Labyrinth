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

    return width, height

def generate_grid(width, height):
    """
    Generates the initial grid for the randomized Kruskal's maze generation algorithm.
    The grid returned is a two-dimensional list of integers.
    Its first dimension is of size the height specified and its second of size the width specified.
    -1 represents walls, numbers from 0 to width * height represent open cells.
    """

    grid = []
    grid.append([-1] * (width * 2 + 1))

    for y in range(height):
        line = []
        line.append(-1)

        for x in range(width):
            line.append(x + y * width)
            line.append(-1)

        grid.append(line)
        grid.append([-1] * (width * 2 + 1))

    return grid

def is_maze_done(grid):
    """
    Returns True if and only if the specified grid only contains -1 and 0.
    This means the randomized Kruskal's maze generation algorithm is completed.
    """

    for line in grid:
        for cell in line:
            if cell != -1 and cell != 0:
                return False

    return True

def get_adjacent_cells(grid, x, y):
    """
    Returns all the adjacent valid cells to the one with the specified coordinates.
    Assumes -1 represents walls and anything else represents open cells.
    """

    adjacent = []

    for dx, dy in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
        if y + dy < 0 or y + dy >= len(grid) or x + dx < 0 or x + dx >= len(grid[y + dy]) or grid[y + dy][x + dx] == -1:
            continue

        adjacent.append((x + dx, y + dy))

    return adjacent

def propagate(grid, x, y):
    """
    If the cell at the specified coordinates is a wall next to an open cell, replaces it with an open cell of the same value.
    Then, merges all the neighboring sets into the smallest one recursively.
    """

    if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[y]):
        return

    minimum = None

    for cell in get_adjacent_cells(grid, x, y):
        if minimum is None or grid[cell[1]][cell[0]] < minimum:
            minimum = grid[cell[1]][cell[0]]

    if minimum is None:
        return

    grid[y][x] = minimum

    for cell in get_adjacent_cells(grid, x, y):
        if grid[cell[1]][cell[0]] > minimum:
            propagate(grid, cell[0], cell[1])

def generate_maze(width, height):
    """
    Generates a maze of the specified size using a derived and randomized form of Kruskal's maze generation algorithm.
    The grid returned is a two-dimensional list of integers.
    Its first dimension is of size the height specified and its second of size the width specified.
    -1 represents walls, spaces (" ") represent open cells.
    """

    grid = generate_grid(width, height)

    while not is_maze_done(grid):
        if random.getrandbits(1):
            # Horizontal
            x = random.randrange(width) * 2 + 1
            y = random.randrange(1, height) * 2

            if grid[y][x] != -1 or grid[y - 1][x] == grid[y + 1][x]:
                continue
        else:
            # Vertical
            x = random.randrange(1, width) * 2
            y = random.randrange(height) * 2 + 1

            if grid[y][x] != -1 or grid[y][x - 1] == grid[y][x + 1]:
                continue

        propagate(grid, x, y)

    for y in range(1, height * 2):
        for x in range(1, width * 2):
            if grid[y][x] == 0:
                grid[y][x] = " "

    return grid

def display_maze(grid):
    """
    Displays the specified maze.
    Cells with -1 are replaced with stars ("*").
    Numbers above 9 are replaced with letters, or plus ("+") if they are above 61.
    """

    characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+"
    for line in grid:
        for cell in line:
            if cell == -1:
                print("*", end=" ")
            else:
                if type(cell) is int:
                    cell = characters[min(cell, len(characters) - 1)]
                print(cell, end=" ")
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

        valid = len(get_adjacent_cells(grid, xA, yA)) == 1
        if not valid:
            print("The starting point (A) must be an external wall adjacent to an empty cell.")

    valid = False
    while not valid:
        print("Enter the coordinates of the ending point (B):")
        xB = int(input("X: "))
        yB = int(input("Y: "))

        valid = len(get_adjacent_cells(grid, xB, yB)) == 1 and (xB != xA or yB != y1)
        if not valid:
            print("The ending point (B) must be an external wall adjacent to an empty cell and different from the starting point.")

    return xA, yA, xB, yB

def get_path(grid, distances, x, y):
    """
    Traces back the path from the specified coordinates to the point of distance 0.
    Returns the grid specified, replacing spaces (" ") with dots (".") along the path.
    WARNING: The distances should only describe one path of decrementing integers from the specified coordinates.
             Otherwise, the behavior is undefined and the function may return None.
    """

    solution = [line.copy() for line in grid]

    d = distances[y][x]
    while d > 0:
        for cell in get_adjacent_cells(distances, x, y):
            if distances[cell[1]][cell[0]] == d - 1:
                x, y = cell
                d -= 1
                break
        else:
            return None

        if solution[cell[1]][cell[0]] == " ":
            solution[cell[1]][cell[0]] = "."

    return solution

def solve_maze(grid, xA, yA, xB, yB):
    """
    Finds the optimal solution of the specified maze grid, where the starting point is (xA, yA) and the exit has coordinates (xB, yB).
    Returns the number of cells explored by the algorithm, the length of the shortest path, as well as the path itself.
    Assumes -1 represents walls and anything else represents open cells.
    The returned grid contains dots (".") along the path.
    """

    distances = [[-1] * len(line) for line in grid]

    explored = 0
    pending, found = [(xA, yA, 0)], False
    while not found and pending:
        x, y, d = pending.pop(0)
        if distances[y][x] != -1:
            if distances[y][x] <= d:
                continue
        else:
            explored += 1
        distances[y][x] = d

        for cell in get_adjacent_cells(grid, x, y):
            if cell[0] == xB and cell[1] == yB:
                distances[yB][xB] = d + 1
                found = True
                break

            pending.append((cell[0], cell[1], d + 1))

    return explored, distances[yB][xB], get_path(grid, distances, xB, yB)

def main():
    """
    Executes the labyrinth program.
    """

    sys.setrecursionlimit(100000)

    width, height = input_maze_size()
    grid = generate_maze(width, height)

    print("Here is the random labyrinth:")
    display_maze(grid)

    xA, yA, xB, yB = input_points(grid)

    grid[yA][xA] = "A"
    grid[yB][xB] = "B"

    explored, length, solution = solve_maze(grid, xA, yA, xB, yB)

    if solution is not None:
        print("Here is the shortest path:")
        display_maze(solution)
        print("Number of explored cells to find the path:", explored)
        print("Length of the shortest path:", length)
    else:
        print("No solution found to the maze.")

if __name__ == "__main__":
    main()
