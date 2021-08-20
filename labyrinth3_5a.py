#!/usr/bin/env python3

import sys
import random

def input_maze_size():
    print("Enter the size of your labyrinth:")

    width = int(input("Width: "))
    height = int(input("Height: "))

    return width, height

def generate_grid(width, height):
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

def is_maze_done(grid, allow_walls):
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[y]) - 1):
            if grid[y][x] != 0 and (not allow_walls or grid[y][x] != -1):
                return False

    return True

def get_adjacent_cells(grid, x, y):
    adjacent = []

    for dx, dy in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
        if y + dy < 0 or y + dy >= len(grid) or x + dx < 0 or x + dx >= len(grid[y + dy]) or grid[y + dy][x + dx] == -1:
            continue

        adjacent.append((x + dx, y + dy))

    return adjacent

def propagate(grid, x, y):
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

def generate_cycles(grid, cycles):
    i = 0
    while i < cycles:
        if is_maze_done(grid, False):
            break

        if random.getrandbits(1):
            # Horizontal
            x = random.randrange(len(grid[0]) // 2) * 2 + 1
            y = random.randrange(1, len(grid) // 2) * 2
        else:
            # Vertical
            x = random.randrange(1, len(grid[0]) // 2) * 2
            y = random.randrange(len(grid) // 2) * 2 + 1

        if grid[y][x] != -1:
            continue

        propagate(grid, x, y)
        i += 1

    return grid

def generate_maze(width, height, cycles):
    grid = generate_grid(width, height)

    while not is_maze_done(grid, True):
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

    grid = generate_cycles(grid, cycles)

    for y in range(1, height * 2):
        for x in range(1, width * 2):
            if grid[y][x] == 0:
                grid[y][x] = " "

    return grid

def display_maze(grid):
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
    sys.setrecursionlimit(100000)

    width, height = input_maze_size()
    cycles = int(input("How many cycles do you want in the maze approximately? "))
    grid = generate_maze(width, height, cycles)

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
