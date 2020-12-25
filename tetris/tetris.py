import curses
import time
from time import sleep
import keyboard
import sys
import numpy as np

class Board():

    def __init__(self, blen, bwidth):

        self.blen = blen
        self.bwidth = bwidth
        
        # board representation
        self.env_map = [[' ' for _ in range(bwidth)] for _ in range(blen)]
        for r in self.env_map:
            r[0] = '#'

        # Initialization settings
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(True)

        # clear screen
        self.stdscr.clear()

        # Draw board
        for i in range(self.blen+1):
            self.stdscr.addstr(i, 0, '#')
            self.stdscr.addstr(i, self.bwidth, '#')

        for i in range(self.bwidth+1):
            self.stdscr.addstr(self.blen, i, '#')

        # Initialize piece settings
        self.piece_loc = []
        self.piece_rot = False
        
        # first piece
        for i in range(3,7):
            self.stdscr.addstr(0, i, '#')
            self.piece_loc.append( [0, i] )

        # refresh screen
        self.stdscr.refresh()


    def Move_Piece(self, k):

        def Write(row, col, piece):
            self.stdscr.addstr(row, col, piece)

        def Erase(row, col):
            self.stdscr.addstr(row, col, ' ')

        if k == curses.KEY_DOWN:
            # if max([i[0] for i in self.piece_loc]) == (self.blen - 1):
                # return

            for i, j in self.piece_loc:
                Erase(i, j)
            for i, j in self.piece_loc:
                Write(i+1, j, '#')

            for n, (i, j) in enumerate(self.piece_loc):
                self.piece_loc[n][0] = i+1

            for i, j in self.piece_loc:
                if (i == self.blen-1) or (self.env_map[i+1][j] == '#'):
                    self.Write_Piece_To_Board()
                    self.Check_Advance_Game()
                    self.Make_New_Piece()

        elif k == curses.KEY_LEFT:
            if min([i[1] for i in self.piece_loc]) == 1:
                return

            for i, j in self.piece_loc:
                Erase(i, j)
            for i, j in self.piece_loc:
                Write(i, j-1, '#')

            for n, (i, j) in enumerate(self.piece_loc):
                self.piece_loc[n][1] = j-1

        elif k == curses.KEY_RIGHT:
            if max([i[1] for i in self.piece_loc]) == (self.bwidth - 1):
                return

            for i, j in self.piece_loc:
                Erase(i, j)
            for i, j in self.piece_loc:
                Write(i, j+1, '#')

            for n, (i, j) in enumerate(self.piece_loc):
                self.piece_loc[n][1] = j+1

        elif k == ord('r'):
            if self.piece_rot == False:
                left_col = min(i[1] for i in self.piece_loc)
                for i, j in self.piece_loc:
                    Erase(i, j)

                for n, (i, j) in enumerate(self.piece_loc):
                    self.piece_loc[n] = [j - left_col + i, left_col]

                for i, j in self.piece_loc:
                    Write(i, j, '#')

                self.piece_rot = True

            else:
                top_row = min(i[0] for i in self.piece_loc)
                for i, j in self.piece_loc:
                    Erase(i, j)

                for n, (i, j) in enumerate(self.piece_loc):
                    self.piece_loc[n] = [top_row, i - top_row + j]

                for i, j in self.piece_loc:
                    Write(i, j, '#')

                self.piece_rot = False


        elif k == ord('q'):
            curses.nocbreak()
            self.stdscr.keypad(False)
            curses.echo()
            curses.endwin()
            sys.exit("Quit game.")



    def Make_New_Piece(self):
        self.piece_loc = []
        self.piece_rot = False

        for i in range(3,7):
            self.stdscr.addstr(0, i, '#')
            self.piece_loc.append( [0, i] )

    def Write_Piece_To_Board(self):
        for p0, p1 in self.piece_loc:
            self.env_map[p0][p1] = '#'

    def Check_Advance_Game(self):
        lowest_row = max([x[0] for x in self.piece_loc])
        if all(p == '#' for p in self.env_map[lowest_row]):
            self.env_map[lowest_row][:] = list(['#'] + [' ' for _ in range(self.bwidth-1)])
            for ind in range(1, self.bwidth):
                self.stdscr.addstr(lowest_row, ind, ' ')





def main():

    b = Board(12, 9)

    b.stdscr.timeout(0) # enables automatic drop of piece after 1 second
    k = b.stdscr.getch()
    while True:
        a = time.time()
        while time.time() - a < 1.5:
            b.Move_Piece(k)
            b.stdscr.refresh()
            k = b.stdscr.getch()
        b.Move_Piece(curses.KEY_DOWN)
        b.stdscr.refresh()
        k = b.stdscr.getch()

# Driver
main()