# Labyrinth

During the first year at [Efrei Paris](https://www.efrei.fr), the first semester's second project in Python was a maze generator and solver.\
Such a program allows to generate mazes of arbitrary sizes, and find a solution either by hand or with multiple automatic algorithms.\
Other complementary functionalities include a scoreboard, the ability to save and restore the game, two additional algorithms to find the shortest path, another generator and solver for 3 dimensional mazes, as well as another for mazes with cycles.\
The project consists of 8 programs. The main file is `labyrinth.py` and contains the logic to generate and solve regular mazes.

## Generation Algorithm

To generate the maze, we can use a derived form of the [randomized Kruskal's maze generation algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Kruskal's_algorithm) to generate mazes which don't contain any cycle.\
If needed, we can afterwards intentionally add a specific amount of cycles, as illustrated in the file `labyrinth3_5.py`.

The generation algorithm can be described with the following steps:
1. Generate a grid (or 2-dimensional array of integers) of `n * 2 + 1` lines and `m * 2 + 1` columns where n and m are the dimensions of the maze requested by the user.
2. Fill this grid with `−1` in all cells with at least one even coordinate.
3. For each remaining cell, fill it with a unique ascending number starting from `0`.
4. While there is at least one cell which is neither `0` nor `−1`, repeat:
	1. Select a wall with exactly one even coordinate which is not an external wall and which only separates cells containing different values.
	2. Remove this wall by replacing it with the lowest of the two adjacent cells.
	3. Propagate this value to all touching cells.

This algorithm can then easily be extended to a third dimension by creating a 3-dimensional array instead of 2 and changing the method used to retrieve adjacent cells, as illustrated in the file `labyrinth3_4.py`.\
To add cycles after we successfully generated a maze, we can simply repeat the operations under step 4 until we get the desired amount of cycles, as illustrated in the file `labyrinth3_5.py`.

## Solving Algorithm

There are many ways to solve a maze automatically. The one used in this project consists in exploring the maze and storing the distance to the starting point for each cell, to then reconstruct the path from the ending point.\
The benefit of this algorithm is that it always finds the shortest path. Its main drawback is that its worst case has the same complexity as its best case, because it has to explore the entire maze before finding the path.\
To fix this issue, we can stop the algorithm as soon as we find the exit point. This means that a correct path was found. In case there are multiple paths (because of cycles), the path found is still the shortest one, because we explore the closest cells to the starting point first. This improvement has been implemented in the file `labyrinth3_2.py`.

Another way to solve a maze automatically is a well known method to find your way out of a maze where the entrance and the exit are both along an external wall. It consists in placing your right (or left) hand on the wall to the right (or left, respectively) and never lifting it.\
In a maze with no cycle, there is only one path between any two points of the maze, which implies that there is only one solution. Thus this algorithm will always find the shortest path if the maze matches the requirements above.\
This algorithm has been implemented in the file `labyrinth3_3.py` which also displays the number of cells explored to find the solution. As we can see, this number is greatly lower (in average) to the number of cells explored by the previous algorithm, which is a great benefit.\
Unfortunately, this algorithm does not allow to always find the shortest path in a maze containing cycles, or in a maze where the starting or ending point aren't along an external wall, so it has to be used carefully.

## Additional Features

The file `labyrinth3_1.py` also contains other functionalities:
1. First, a scoreboard is kept in the `scoreboard.csv` file. It contains several data points from all the games played with this version. The entries are ordered by descending score, to get the best games on top. This file can be opened with Excel for example, and will show you all the information on each game including the date (a unix timestamp) of when this game ended, the time spent by the user, the number of cells they explored, the length of the path found by the user and the shortest one, and their final score.
2. Secondly, if you press Ctrl+C while playing, the state of the labyrinth will be stored and when you execute it again, the game resumes playing along with the game's timer. This was done using the pickle Python module which allows to store and read data in a file persistently.

A Graphical User Interface proof of concept was also created in the file `labyrinth3_1.py`, which allows the selection of the size of the labyrinth, the entry and exit points and the resolution of the labyrinth by the user or the computer automatically. Unfortunately, the technologies used (Tkinter) does not provide a fast enough rendering engine, making the game generally very slow. This could be fixed by switching to another library, or by reusing existing components on the screen such as the cells in the labyrinth, and only changing their content.

A `benchmark.py` is included and allows to compare the three different types of pathfinding algorithms. Here is a sample output:
> Algorithm 1: 5101.000000 average cells explored, 264.752000 average path length, 0.026539 average execution time
> Algorithm 2: 4948.308000 average cells explored, 264.752000 average path length, 0.026494 average execution time
> Algorithm 3: 1353.812000 average cells explored, 446.236000 average path length, 0.007047 average execution time

The last algorithm, the right-hand one, is almost 4 times faster than the other two on average, but does not guarantee to find the shortest path in a maze with cycles. The two others are almost equivalent, with a slight speed increase in the second, as it stops as soon as it finds the exit rather than explore the entire maze each time.
