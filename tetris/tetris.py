import curses
# from curses import wrapper

class Board():

    def __init__(self, blen, bwidth):

        self.blen = blen
        self.bwidth = bwidth
        
        # board representation
        self.env_map = [[' ' for _ in range(bwidth)] for _ in range(blen)]
        self.piece_loc = []
        self.piece_rot = False

        # Initialization settings
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(True)

        # clear screen
        self.stdscr.clear()

        # Draw board
        for i in range(0, self.blen+1):
            self.stdscr.addstr(i, 0, '#')
            self.stdscr.addstr(i, self.bwidth, '#')

        for i in range(0, self.bwidth+1):
            self.stdscr.addstr(self.blen, i, '#')

        # test piece
        for i in range(3,7):
            self.stdscr.addstr(0, i, '#')
            self.piece_loc.append( [0, i] )

        self.stdscr.refresh()


    def Move_Piece(self, k):

        def Write(row, col, piece):
            self.stdscr.addstr(row, col, piece)

        def Erase(row, col):
            self.stdscr.addstr(row, col, ' ')

        if k == curses.KEY_DOWN:
            if max([i[0] for i in self.piece_loc]) == (self.blen - 1):
                return

            for i, j in self.piece_loc:
                Erase(i, j)
            for i, j in self.piece_loc:
                Write(i+1, j, '#')

            for n, (i, j) in enumerate(self.piece_loc):
                self.piece_loc[n][0] = i+1

        elif k == curses.KEY_UP:
            if min([i[0] for i in self.piece_loc]) == 0:
                return

            for i, j in self.piece_loc:
                Erase(i, j)
            for i, j in self.piece_loc:
                Write(i-1, j, '#')

            for n, (i, j) in enumerate(self.piece_loc):
                self.piece_loc[n][0] = i-1

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







def main():

    b = Board(12, 18)

    k = b.stdscr.getch()
    while k != ord('q'):
        b.Move_Piece(k)
        b.stdscr.refresh()
        k = b.stdscr.getch()

    # # end program
    curses.nocbreak()
    b.stdscr.keypad(False)
    curses.echo()
    curses.endwin()

main()