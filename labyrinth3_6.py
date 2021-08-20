#!/usr/bin/env python3

import sys
import time
import random
import tkinter
import traceback
from tkinter import messagebox

def input_maze_size(screen, callback):
    """
    Inputs and returns two integers from the user.
    They represent the width and the height of the labyrinth, respectively.
    """

    widthValue = tkinter.IntVar()
    heightValue = tkinter.IntVar()

    def generate_callback():
        for widget in screen.winfo_children():
            widget.destroy()

        screen.grid_rowconfigure(0, weight=0)
        screen.grid_rowconfigure(5, weight=0)
        screen.grid_columnconfigure(0, weight=0)
        screen.grid_columnconfigure(3, weight=0)

        callback(widthValue.get(), heightValue.get())

    titleLabel = tkinter.Label(screen, text="Enter the size of your labyrinth:")
    titleLabel.grid(row=1, column=1, columnspan=2)

    widthScale = tkinter.Scale(screen, from_=2, to=32, variable=widthValue, orient=tkinter.HORIZONTAL)
    widthScale.set(16)

    heightScale = tkinter.Scale(screen, from_=2, to=20, variable=heightValue, orient=tkinter.HORIZONTAL)
    heightScale.set(10)

    widthLabel = tkinter.Label(screen, text="Width: ")
    heightLabel = tkinter.Label(screen, text="Height: ")

    widthLabel.grid(row=2, column=1)
    widthScale.grid(row=2, column=2)
    heightLabel.grid(row=3, column=1)
    heightScale.grid(row=3, column=2)

    generateButton = tkinter.Button(screen, text="Generate", command=generate_callback)
    generateButton.grid(row=4, column=1, columnspan=2)

    screen.grid_rowconfigure(0, weight=1)
    screen.grid_rowconfigure(5, weight=1)
    screen.grid_columnconfigure(0, weight=1)
    screen.grid_columnconfigure(3, weight=1)

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

def display_maze(screen, grid, title=None):
    """
    Displays the specified maze.
    Cells with -1 are replaced with stars ("*").
    Numbers above 9 are replaced with letters, or plus ("+") if they are above 61.
    """

    for widget in screen.winfo_children():
        widget.destroy()

    frame = tkinter.Frame(screen)

    if title is not None:
        titleLabel = tkinter.Label(frame, text=title)
        titleLabel.grid(row=0, column=0, columnspan=len(grid[0]))

    characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+"
    for y, line in enumerate(grid):
        for x, cell in enumerate(line):
            if cell == -1:
                cell = "*"
            elif type(cell) is int:
                cell = characters[min(cell, len(characters) - 1)]
            else:
                cell = str(cell)

            cellLabel = tkinter.Label(frame, textvariable=tkinter.StringVar(frame, cell))
            cellLabel.grid(row=y + 1, column=x)

    frame.grid(row=0, column=0)
    screen.grid_rowconfigure(0, weight=1)
    screen.grid_columnconfigure(0, weight=1)

def input_points(screen, grid, callback):
    """
    Inputs and returns four integers from the user.
    The first two represent the x and y coordinates of the labyrinth's entrance respectively.
    The last two represent the x and y coordinates of the labyrinth's exit respectively.
    """

    display_maze(screen, grid, "Here is the random labyrinth:")

    xAValue = tkinter.IntVar()
    yAValue = tkinter.IntVar()

    xBValue = tkinter.IntVar()
    yBValue = tkinter.IntVar()

    def place_callback():
        if len(get_adjacent_cells(grid, xAValue.get(), yAValue.get())) != 1:
            messagebox.showerror("Labyrinth Project", "ERROR!\nThe starting point (A) must be an external wall adjacent to an empty cell.")
            return

        if len(get_adjacent_cells(grid, xBValue.get(), yBValue.get())) != 1:
            messagebox.showerror("Labyrinth Project", "ERROR!\nThe ending point (B) must be an external wall adjacent to an empty cell.")
            return

        if xAValue.get() == xBValue.get() and yAValue.get() == yBValue.get():
            messagebox.showerror("Labyrinth Project", "ERROR!\nThe starting point (A) must be different from the ending point (B).")
            return

        for widget in screen.winfo_children():
            widget.destroy()

        screen.grid_rowconfigure(0, weight=0)
        screen.grid_rowconfigure(8, weight=0)
        screen.grid_columnconfigure(0, weight=0)
        screen.grid_columnconfigure(3, weight=0)

        grid[yAValue.get()][xAValue.get()] = "A"
        grid[yBValue.get()][xBValue.get()] = "B"

        callback(grid, xAValue.get(), yAValue.get(), xBValue.get(), yBValue.get())

    titleALabel = tkinter.Label(screen, text="Enter the coordinates of the starting point (A):")
    titleALabel.grid(row=1, column=1, columnspan=2)

    xAScale = tkinter.Scale(screen, from_=0, to=len(grid[0]) - 1, variable=xAValue, orient=tkinter.HORIZONTAL)
    xAScale.set(0)

    yAScale = tkinter.Scale(screen, from_=0, to=len(grid) - 1, variable=yAValue, orient=tkinter.HORIZONTAL)
    yAScale.set(1)

    xALabel = tkinter.Label(screen, text="X: ")
    yALabel = tkinter.Label(screen, text="Y: ")

    xALabel.grid(row=2, column=1)
    xAScale.grid(row=2, column=2)
    yALabel.grid(row=3, column=1)
    yAScale.grid(row=3, column=2)

    titleBLabel = tkinter.Label(screen, text="Enter the coordinates of the ending point (B):")
    titleBLabel.grid(row=4, column=1, columnspan=2)

    xBScale = tkinter.Scale(screen, from_=0, to=len(grid[0]) - 1, variable=xBValue, orient=tkinter.HORIZONTAL)
    xBScale.set(len(grid[0]) - 1)

    yBScale = tkinter.Scale(screen, from_=0, to=len(grid) - 1, variable=yBValue, orient=tkinter.HORIZONTAL)
    yBScale.set(len(grid) - 2)

    xBLabel = tkinter.Label(screen, text="X: ")
    yBLabel = tkinter.Label(screen, text="Y: ")

    xBLabel.grid(row=5, column=1)
    xBScale.grid(row=5, column=2)
    yBLabel.grid(row=6, column=1)
    yBScale.grid(row=6, column=2)

    placeButton = tkinter.Button(screen, text="Place", command=place_callback)
    placeButton.grid(row=7, column=1, columnspan=2)

    screen.grid_rowconfigure(0, weight=1)
    screen.grid_rowconfigure(8, weight=1)
    screen.grid_columnconfigure(0, weight=1)
    screen.grid_columnconfigure(3, weight=1)

def input_move(screen, callback):
    """
    Inputs a move from the user.
    Returns the delta in x and delta in y of the move, where the origin (0, 0) is at the top left corner.
    """

    def press_callback(event):
        screen.unbind("<Any-KeyPress>")

        if event.keysym == "Up":
            callback(0, -1)
        elif event.keysym == "Down":
            callback(0, +1)
        elif event.keysym == "Left":
            callback(-1, 0)
        elif event.keysym == "Right":
            callback(+1, 0)

    screen.bind("<Any-KeyPress>", press_callback)

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

def player_solve_maze(screen, grid, xA, yA, xB, yB, callback):
    """
    Allows the user to solve the specified maze grid, where the starting point is (xA, yA) and the exit has coordinates (xB, yB).
    Returns the number of moves the user needed to find the path, the length of the path found by the user, as well as the path itself.
    Assumes -1 represents walls and anything else represents open cells.
    The returned grid contains dots (".") along the path.
    """

    distances = [[-1] * len(line) for line in grid]
    distances[yA][xA] = 0

    def move_callback(distances, x, y, d, found, explored, dx, dy):
        if y + dy < 0 or y + dy >= len(grid) or x + dx < 0 or x + dx >= len(grid[y + dy]) or grid[y + dy][x + dx] == -1:
            input_move(screen, lambda dx, dy: move_callback(distances, x, y, d, found, explored, dx, dy))
            return

        if distances[y + dy][x + dx] != -1:
            d = distances[y + dy][x + dx]
            rollback(distances, x, y, d)

        x += dx
        y += dy
        distances[y][x] = d
        explored += 1
        d += 1

        if x == xB and y == yB:
            callback(explored, distances[yB][xB], get_path(grid, distances, xB, yB))
            return

        solution = get_path(grid, distances, x, y)
        if solution is not None:
            solution[y][x] = "X"
            display_maze(screen, solution)

        input_move(screen, lambda dx, dy: move_callback(distances, x, y, d, found, explored, dx, dy))

    move_callback(distances, xA, yA, 1, False, 0, 0, 0)

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

def input_maze(screen, callback):
    """
    Inputs the required information from the user to generate a maze.
    Returns the generated maze's grid.
    -1 represents walls, spaces (" ") represent open cells.
    The entrance and exit are marked with "A" and "B" respectively.
    """

    input_maze_size(screen, lambda width, height: input_points(screen, generate_maze(width, height), callback))

def play(screen, grid, xA, yA, xB, yB):
    """
    Asks the user if he wishes to solve the maze himself or to find the solution automatically.
    Then, performs as requested using the specified information, and outputs some statistics.
    """

    answer = messagebox.askyesno("Labyrinth Project", "Do you want to solve the maze (Yes) or want the computer to give you the solution (No)?")

    computer_explored, computer_length, computer_solution = computer_solve_maze(grid, xA, yA, xB, yB)
    if computer_solution is not None:
        if answer:
            def player_solve_maze_callback(explored, length, solution):
                end = time.time()
                elapsed = end - start
                score = computer_length / length * 2 ** -(elapsed / (len(grid) * len(grid[0]))) * 100

                display_maze(screen, computer_solution, "Here was the shortest path:")
                print("Number of explored cells to find your path: {}\nLength of your path: {}\nTime to find your path: {:.2f} seconds\n".format(explored, length, elapsed))
                print("Number of explored cells to find the shortest path: {}\nLength of the shortest path: {}\n".format(computer_explored, computer_length))
                print("Score: {:.2f} points".format(score))

            start = time.time()
            player_solve_maze(screen, grid, xA, yA, xB, yB, player_solve_maze_callback)
        else:
            display_maze(screen, computer_solution, "Here is the shortest path:")
            print("Number of explored cells to find the path: {}\nLength of the shortest path: {}".format(computer_explored, computer_length))
    else:
        print("No solution found to the maze.")

def main():
    """
    Executes the labyrinth program.
    """

    screen = tkinter.Tk()
    screen.title("Labyrinth Project")
    screen.geometry("800x500")

    sys.setrecursionlimit(100000)

    input_maze(screen, lambda grid, xA, yA, xB, yB: play(screen, grid, xA, yA, xB, yB))

    screen.mainloop()

if __name__ == "__main__":
    main()
