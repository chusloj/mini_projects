import curses
from curses import wrapper

class Board():
    def __init__(self, blen, bwidth):
        self.blen = blen
        self.bwidth = bwidth
        self.piece_col = 3
        self.piece_row = 0

        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(True)

        self.stdscr.clear()

    def Draw_Board(self):
        for i in range(0, self.blen+1):
            self.stdscr.addstr(i, 0, '#')
            self.stdscr.addstr(i, self.bwidth, '#')

        for i in range(0, self.bwidth+1):
            self.stdscr.addstr(self.blen, i, '#')

    def Move_Piece(self, c):
        if c == curses.KEY_DOWN:
            if self.piece_row == (self.blen - 1):
                return
            for i in range(self.piece_col, self.piece_col + 4):
                self.stdscr.addstr(self.piece_row, i, ' ')
                self.stdscr.addstr(self.piece_row+1, i, '#')
            self.piece_row += 1
        elif c == curses.KEY_UP:
            if self.piece_row == 0:
                return
            for i in range(self.piece_col, self.piece_col + 4):
                self.stdscr.addstr(self.piece_row, i, ' ')
                self.stdscr.addstr(self.piece_row-1, i, '#')
            self.piece_row -= 1
        elif c == curses.KEY_LEFT:
            if (self.piece_col - 1) == 0:
                return
            for i in range(self.piece_col, self.piece_col + 4):
                self.stdscr.addstr(self.piece_row, i, ' ')
            for i in range(self.piece_col - 1, self.piece_col + 3):
                self.stdscr.addstr(self.piece_row, i, '#')
            self.piece_col -= 1
        elif c == curses.KEY_RIGHT:
            if (self.piece_col + 4) == self.bwidth:
                return
            for i in range(self.piece_col, self.piece_col + 4):
                self.stdscr.addstr(self.piece_row, i, ' ')
            for i in range(self.piece_col + 1, self.piece_col + 5):
                self.stdscr.addstr(self.piece_row, i, '#')
            self.piece_col += 1
        elif c == ord('r'):
            for i in range(self.piece_col, self.piece_col + 4):
                self.stdscr.addstr(self.piece_row, i, ' ')
            for i in range(self.piece_row, self.piece_row + 4):
                self.stdscr.addstr(i, self.piece_col, '#')

    def Rotate_Piece(self):
        for i in range(self.piece_col, self.piece_col + 4):
            self.stdscr.addstr(self.piece_row, i, ' ')
        for i in range(self.piece_row, self.piece_row + 4):
            self.stdscr.addstr(i, self.piece_col, '#')



def main():
    # Initialize
    b = Board(12, 18)

    b.Draw_Board()

    # # draw tetromino
    for i in range(3,7):
        b.stdscr.addstr(0, i, '#')

    c = b.stdscr.getch()
    while c != ord('q'):
        b.Move_Piece(c)
        b.stdscr.refresh()
        c = b.stdscr.getch()

    # # end program
    curses.nocbreak()
    b.stdscr.keypad(False)
    curses.echo()
    curses.endwin()


main()