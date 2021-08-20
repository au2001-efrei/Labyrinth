#!/usr/bin/env python3

import sys
import time
import labyrinth
import labyrinth3_2
import labyrinth3_3
import labyrinth3_5

def main():
    sys.setrecursionlimit(100000)

    n = 1000
    width, height, cycles = 50, 50, 100
    xA, yA, xB, yB = 1, 0, 100, 99

    algs = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    funcs = [labyrinth.computer_solve_maze, labyrinth3_2.solve_maze, labyrinth3_3.solve_maze]

    start = time.time()
    for t in range(n):
        grid = labyrinth3_5.generate_maze(width, height, cycles)
        grid[yA][xA] = "A"
        grid[yB][xB] = "B"

        for i in range(len(algs)):
            funcStart = time.time()
            explored, length, solution = funcs[i](grid, xA, yA, xB, yB)
            if solution is None:
                continue
            funcEnd = time.time()
            elapsed = funcEnd - funcStart

            algs[i][0] += explored
            algs[i][1] += length
            algs[i][2] += elapsed
            algs[i][3] += 1

        elapsed = time.time() - start
        print("\rProgress: %d / %d (%f%%) - Elapsed: %f seconds - Remaining: %f seconds" % (t + 1, n, (t + 1) / n * 100, elapsed, elapsed / (t + 1) * (n - t - 1)), end="")
    print()

    for i in range(len(algs)):
        print("Algorithm %d: %f average cells explored, %f average path length, %f average execution time" % (i + 1, algs[i][0] / algs[i][3], algs[i][1] / algs[i][3], algs[i][2] / algs[i][3]))

if __name__ == "__main__":
    main()
