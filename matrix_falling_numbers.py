import numpy as np
import curses, os, time, random
from time import sleep

def Print_New_Nums(grid):
	"""
	Print new numbers for the top of screen
	"""
	for col in range(grid.shape[1]):
		grid[0, col] = ' '
	rand_indices = [random.randint(0, grid.shape[1] - 1) for _ in range(10, 50)]
	for col in range(grid.shape[1]):
		if col in rand_indices:
			grid[0, col] = random.randint(0, 9)

	return grid


def Update_Time_Step(grid):
	"""
	Move all values down one row
	"""
	for row in range(grid.shape[0] - 1, -1, -1):
		for col in range(grid.shape[1]):
			if row == 0:
				grid = Print_New_Nums(grid)
			else:
				grid[row, col] = grid[row - 1, col]

	return grid

def Refresh_Screen(grid):
	"""
	Refresh the entire screen
	using the updated grid
    """
	for row, col in np.ndindex(grid.shape):
		screen.addstr(row, col, grid[row, col])

	screen.refresh()



if __name__ == "__main__":

	# Initialization settings
	screen = curses.initscr()
	curses.noecho()
	curses.cbreak()
	curses.curs_set(0)

	screen.clear()


	rows, cols = screen.getmaxyx()

	grid = [[' ' for _ in range(cols - 5)] for _ in range(rows - 5)]
	grid = np.matrix(grid)

	wait_time = 0.17

	Print_New_Nums(grid)
	time.sleep(wait_time)
	while True:
		grid = Update_Time_Step(grid)
		Refresh_Screen(grid)
		time.sleep(wait_time)
