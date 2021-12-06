import numpy as np
import curses, os, time
from time import sleep


def Update_Grid(current_grid, gridsize):

	next_grid = np.zeros(shape = gridsize, dtype=int)
	for row, col in np.ndindex(current_grid.shape):

		neighbor_count = np.sum(current_grid[row-1:row+2, col-1:col+2]) - current_grid[row, col]

		if (current_grid[row, col] == 1) and (neighbor_count in (2, 3)):
			next_grid[row, col] = 1
		elif (current_grid[row, col] == 1) and (neighbor_count not in (2, 3)):
			next_grid[row, col] = 0
		elif (current_grid[row, col] == 0) and (neighbor_count == 3):
			next_grid[row, col] = 1

	return next_grid


def Process_Grid(grid, gridsize):

	for row, col in np.ndindex(grid.shape):
		if grid[row, col] == 1:
			screen.addstr(row, col, "1")
		elif grid[row, col] == 0:
			screen.addstr(row, col, ' ')

	screen.refresh()


if __name__ == "__main__":

	gridsize = (15, 20)
	grid = np.random.randint(2, size = gridsize, dtype=int)
	sleep_time = 0.17

	max_turns = 50

	# Initialization settings
	screen = curses.initscr()
	curses.noecho()
	curses.cbreak()
	curses.curs_set(0)

	screen.clear()

	Process_Grid(grid, gridsize)

	for _ in range(max_turns):
		grid = Update_Grid(grid, gridsize)
		Process_Grid(grid, gridsize)
		time.sleep(sleep_time)

	