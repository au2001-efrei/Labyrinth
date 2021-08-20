#!/usr/bin/env python3

import os
import sys
import time
import random
import curses
import pickle
import traceback

def input_int(screen, prefix, validate):
    """
    Inputs an integer from the user after displaying the specified prefix.
    If the input is not an integer or if the validate function returns False, asks another input.
    """

    curses.echo()

    result = None
    while result is None or not validate(result):
        screen.addstr("\r" + prefix)
        try:
            result = int(screen.getstr().decode("utf8"))
        except ValueError:
            pass

    curses.noecho()

    return result

def input_maze_size(screen):
    """
    Inputs and returns two integers from the user.
    They represent the width and the height of the labyrinth, respectively.
    """

    screen.addstr("Enter the size of your labyrinth:\n\r")

    width = input_int(screen, "Width: ", lambda x: x > 0)
    height = input_int(screen, "Height: ", lambda x: x > 0)

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

def display_maze(screen, grid):
    """
    Displays the specified maze.
    Cells with -1 are replaced with stars ("*").
    Numbers above 9 are replaced with letters, or plus ("+") if they are above 61.
    """

    characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+"
    for line in grid:
        for cell in line:
            if cell == -1:
                screen.addstr("*")
            elif type(cell) is int:
                screen.addstr(characters[min(cell, len(characters) - 1)])
            else:
                screen.addstr(cell)

            screen.addstr(" ")

        screen.addstr("\n\r")

def input_points(screen, grid):
    """
    Inputs and returns four integers from the user.
    The first two represent the x and y coordinates of the labyrinth's entrance respectively.
    The last two represent the x and y coordinates of the labyrinth's exit respectively.
    """

    valid = False
    while not valid:
        screen.addstr("Enter the coordinates of the starting point (A):\n\r")
        xA = input_int(screen, "X: ", lambda x: x >= 0 and x < len(grid))
        yA = input_int(screen, "Y: ", lambda x: x >= 0 and x < len(grid[0]))

        valid = len(get_adjacent_cells(grid, xA, yA)) == 1
        if not valid:
            screen.addstr("The starting point (A) must be an external wall adjacent to an empty cell.\n\r")

    valid = False
    while not valid:
        screen.addstr("Enter the coordinates of the ending point (B):\n\r")
        xB = input_int(screen, "X: ", lambda x: x >= 0 and x < len(grid))
        yB = input_int(screen, "Y: ", lambda x: x >= 0 and x < len(grid[0]))

        valid = len(get_adjacent_cells(grid, xB, yB)) == 1 and (xB != xA or yB != y1)
        if not valid:
            screen.addstr("The ending point (B) must be an external wall adjacent to an empty cell and different from the starting point.\n\r")

    return xA, yA, xB, yB

def input_move(screen):
    """
    Inputs a move from the user.
    Returns the delta in x and delta in y of the move, where the origin (0, 0) is at the top left corner.
    """

    key = None
    while key not in ["KEY_UP", "KEY_DOWN", "KEY_LEFT", "KEY_RIGHT"]:
        key = screen.getkey()

    if key == "KEY_UP":
        return (0, -1)
    elif key == "KEY_DOWN":
        return (0, +1)
    elif key == "KEY_LEFT":
        return (-1, 0)
    elif key == "KEY_RIGHT":
        return (+1, 0)

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

def rollback(distances, x, y, n):
    """
    Traces back the path from the specified coordinates to the point of distance n.
    Returns the grid specified, with -1 along the path.
    WARNING: The distances should only describe one path of decrementing integers from the specified coordinates.
             Otherwise, the behavior is undefined and the function may return None.
    """

    distances = [line.copy() for line in distances]

    d = distances[y][x]
    distances[y][x] = -1

    while d > n:
        for cell in get_adjacent_cells(distances, x, y):
            if distances[cell[1]][cell[0]] == d - 1:
                x, y = cell
                distances[y][x] = -1
                d -= 1
                break
        else:
            return None

    return distances

def player_move(screen, distances, grid, x, y, d):
    """
    Inputs a move from the user and move the current position accordingly.
    Returns the new distances grid, positions, and path length.
    """

    dx, dy = input_move(screen)
    while y + dy < 0 or y + dy >= len(grid) or x + dx < 0 or x + dx >= len(grid[y + dy]) or grid[y + dy][x + dx] == -1:
        dx, dy = input_move(screen)

    if distances[y + dy][x + dx] != -1:
        d = distances[y + dy][x + dx]
        rollback(distances, x, y, d)

    x, y = x + dx, y + dy
    distances[y][x] = d
    d += 1

    return distances, x, y, d

def save_progress(grid, xA, yA, xB, yB, distances, x, y, explored, elapsed):
    """
    Saves the user's progress to a file so that he can resume it later.
    """

    with open("labyrinth.save", "wb") as file:
        pickle.dump(grid, file)
        pickle.dump((xA, yA), file)
        pickle.dump((xB, yB), file)
        pickle.dump(distances, file)
        pickle.dump((x, y), file)
        pickle.dump(explored, file)
        pickle.dump(elapsed, file)

def load_progress():
    """
    Loads the user's progress from a file which was saved earlier.
    """

    grid, xA, yA, xB, yB, distances, x, y, explored, elapsed = None, -1, -1, -1, -1, None, -1, -1, 0, 0

    try:
        with open("labyrinth.save", "rb") as file:
            grid = pickle.load(file)
            xA, yA = pickle.load(file)
            xB, yB = pickle.load(file)
            distances = pickle.load(file)
            x, y = pickle.load(file)
            explored = pickle.load(file)
            elapsed = pickle.load(file)

        os.remove("labyrinth.save")
    except FileNotFoundError:
        pass

    return grid, xA, yA, xB, yB, distances, x, y, explored, elapsed

def player_solve_maze(screen, grid, xA, yA, xB, yB, distances, x, y, explored, elapsed):
    """
    Allows the user to solve the specified maze grid, starting from (x, y) and where the exit has coordinates (xB, yB).
    Returns the number of moves the user needed to find the path, the length of the path found by the user, as well as the path itself.
    Assumes -1 represents walls and anything else represents open cells.
    The returned grid contains dots (".") along the path.
    """

    if distances is None:
        distances = [[-1] * len(line) for line in grid]

    if x < 0 or y < 0:
        x, y = xA, yA

    if distances[y][x] == -1:
        distances[y][x] = 0

    d = distances[y][x] + 1

    start = time.time()
    try:
        found = False
        while not found:
            solution = get_path(grid, distances, x, y)
            solution[y][x] = "X"
            screen.clear()
            display_maze(screen, solution)

            distances, x, y, d = player_move(screen, distances, grid, x, y, d)
            explored += 1
            found = x == xB and y == yB

        screen.clear()
        return explored, distances[yB][xB], get_path(grid, distances, xB, yB), time.time() - start + elapsed
    except KeyboardInterrupt as e:
        save_progress(grid, xA, yA, xB, yB, distances, x, y, explored, time.time() - start + elapsed)
        raise e

def computer_solve_maze(grid, xA, yA, xB, yB):
    """
    Finds the optimal solution of the specified maze grid, where the starting point is (xA, yA) and the exit has coordinates (xB, yB).
    Returns the number of cells explored by the algorithm, the length of the shortest path, as well as the path itself.
    Assumes -1 represents walls and anything else represents open cells.
    The returned grid contains dots (".") along the path.
    """

    distances = [[-1] * len(line) for line in grid]

    explored = 0
    pending = [(xA, yA, 0)]
    while pending:
        x, y, d = pending.pop(0)
        if distances[y][x] != -1 and distances[y][x] <= d:
            continue
        distances[y][x] = d
        explored += 1

        for cell in get_adjacent_cells(grid, x, y):
            pending.append((cell[0], cell[1], d + 1))

    return explored, distances[yB][xB], get_path(grid, distances, xB, yB)

def input_maze(screen):
    """
    Inputs the required information from the user to generate a maze.
    Returns the generated maze's grid.
    -1 represents walls, spaces (" ") represent open cells.
    The entrance and exit are marked with "A" and "B" respectively.
    """

    width, height = input_maze_size(screen)
    grid = generate_maze(width, height)

    screen.addstr("Here is the random labyrinth:\n\r")
    display_maze(screen, grid)

    xA, yA, xB, yB = input_points(screen, grid)

    grid[yA][xA] = "A"
    grid[yB][xB] = "B"

    return grid, xA, yA, xB, yB

def register_scoreboard(explored, length, elapsed, computer_explored, computer_length, score):
    """
    Creates an entry in the scoreboard with the specified values.
    """

    timestamp = time.time()
    if os.path.exists("scoreboard.csv"):
        scoreboard, inserted = [], False

        with open("scoreboard.csv", "r") as file:
            next(file)
            for line in file:
                entry = list(map(float, line.split(", ")))
                entry[0], entry[3], entry[6] = float(entry[0]), float(entry[3]), float(entry[6])
                entry[1:3], entry[4:6] = map(int, entry[1:3]), map(int, entry[4:6])

                if not inserted and entry[6] < score:
                    scoreboard.append([timestamp, explored, length, elapsed, computer_explored, computer_length, score])
                    inserted = True

                scoreboard.append(entry)

        if not inserted:
            scoreboard.append([timestamp, explored, length, elapsed, computer_explored, computer_length, score])

        with open("scoreboard.csv", "w") as file:
            file.write("timestamp, explored, length, elapsed, computer_explored, computer_length, score\n")
            for entry in scoreboard:
                file.write(", ".join(map(str, entry)) + "\n")
    else:
        entry = [timestamp, explored, length, elapsed, computer_explored, computer_length, score]
        with open("scoreboard.csv", "w") as file:
            file.write("timestamp, explored, length, elapsed, computer_explored, computer_length, score\n")
            file.write(", ".join(map(str, entry)) + "\n")

def play(screen, grid, xA, yA, xB, yB, distances, x, y, explored, elapsed):
    """
    Asks the user if he wishes to solve the maze himself or to find the solution automatically.
    Then, performs as requested using the specified information, and outputs some statistics.
    """

    if distances is None:
        screen.addstr("Do you want to solve the maze (y) or want the computer to give you the solution (n)? ")
        key = None
        while key not in ["y", "Y", "n", "N"]:
            key = screen.getkey()
    else:
        key = "y"

    computer_explored, computer_length, computer_solution = computer_solve_maze(grid, xA, yA, xB, yB)
    if computer_solution is not None:
        if key in ["y", "Y"]:
            explored, length, solution, elapsed = player_solve_maze(screen, grid, xA, yA, xB, yB, distances, x, y, explored, elapsed)

            score = computer_length / length * 2 ** -(elapsed / (len(grid) * len(grid[0]))) * 100
            register_scoreboard(explored, length, elapsed, computer_explored, computer_length, score)

            screen.clear()
            screen.addstr("Here was the shortest path:\n\r")
            display_maze(screen, computer_solution)
            screen.addstr("Number of explored cells to find your path: {}\n\rLength of your path: {}\n\rTime to find your path: {0:.2f} seconds\n\r\n\r".format(explored, length, int(elapsed)))
            screen.addstr("Number of explored cells to find the shortest path: {}\n\rLength of the shortest path: {}\n\r\n\r".format(computer_explored, computer_length))
            screen.addstr("Score: {0:.2f} points\n\r".format(score))
        else:
            screen.clear()
            screen.addstr("Here is the shortest path:\n\r")
            display_maze(screen, computer_solution)
            screen.addstr("Number of explored cells to find the path: {}\n\rLength of the shortest path: {}\n\r".format(computer_explored, computer_length))
    else:
        screen.addstr("No solution found to the maze.\n\r")

def main(screen=None):
    """
    Executes the labyrinth program.
    """

    if screen is None:
        try:
            curses.wrapper(main)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print("Oops! An error occured:", e)
            traceback.print_exc()
        return

    sys.setrecursionlimit(100000)

    curses.start_color()
    curses.use_default_colors()

    grid, xA, yA, xB, yB, distances, x, y, explored, elapsed = load_progress()
    if grid is None:
        grid, xA, yA, xB, yB = input_maze(screen)

    play(screen, grid, xA, yA, xB, yB, distances, x, y, explored, elapsed)

    screen.addstr("Press any key to quit.")
    screen.getkey()

if __name__ == "__main__":
    main()
