import curses, keyboard, sys, random
import os
import time
from time import sleep
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

        # Draw instructions
        move_inst = "MOVE: Down, Left, Right keys"
        rot_inst = "ROTATE: r"
        quit_inst = "QUIT: q"
        self.stdscr.addstr(5, self.bwidth+5, move_inst)
        self.stdscr.addstr(6, self.bwidth+5, rot_inst)
        self.stdscr.addstr(7, self.bwidth+5, quit_inst)
        
        # piece characteristics
        self.piece_style = None
        self.piece_loc = []
        self.piece_rot = False
        self.piece_rot_setting = None

        # first piece
        self.game_start = True
        self.Generate_Piece('Random')
        self.game_start = False

        # refresh screen
        self.stdscr.refresh()


    def Generate_Piece(self, choice='Random'):
        

        if self.game_start == False:
            self.piece_loc = []
            self.piece_rot = False
            self.piece_rot_setting = None

        if choice == 'Random':
            
            for r in self.env_map[0:2]:
                if any(p == '#' for p in r[1:]):
                    self.Generate_Piece('a')
                    return

            else:
                self.Generate_Piece(random.choice(['a', 'b', 'c']))

        elif choice == 'a':
            self.piece_style = 'a'

            for i in range(3,7):
                self.stdscr.addstr(0, i, '#')
                self.piece_loc.append( [0, i] )
        
        elif choice == 'b':
            self.piece_style = 'b'

            for i in range(4,7):
                self.stdscr.addstr(1, i, '#')
                self.piece_loc.append( [1, i] )

            self.stdscr.addstr(0, 5, '#')
            self.piece_loc.append( [0, 5])

        elif choice == 'c':
            self.piece_style = 'c'

            piece_list = [[0, 4], [0, 5], [1, 4], [1, 5]]
            for i, j in piece_list:
                self.stdscr.addstr(i, j, '#')
                self.piece_loc.append([i, j])
            del piece_list


    
    def Move_Piece(self, k):

        def Write(row, col, piece):
            self.stdscr.addstr(row, col, piece)

        def Erase(row, col):
            self.stdscr.addstr(row, col, ' ')


        if k == curses.KEY_DOWN:

            self.Check_End_Of_Game()

            for i, j in self.piece_loc:
                Erase(i, j)
            
            for i, j in self.piece_loc:
                Write(i+1, j, '#')

            for n, (i, j) in enumerate(self.piece_loc):
                self.piece_loc[n][0] = i+1


            if not any(i == self.blen-1 for i, j in self.piece_loc):
                if any((self.env_map[i+1][j] == '#') for i, j in self.piece_loc):
                    self.Write_Piece_To_Board()
                    self.Check_Advance_Game()
                    self.Generate_Piece()
            else:
                self.Write_Piece_To_Board()
                self.Check_Advance_Game()
                self.Generate_Piece()

        elif k == curses.KEY_LEFT:

            if min([i[1] for i in self.piece_loc]) == 1:
                return

            left_barrier = min(i[1] for i in self.piece_loc)
            for r in [i[0] for i in self.piece_loc]:
                if '#' in self.env_map[r][left_barrier - 1]:
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

            right_barrier = max(i[1] for i in self.piece_loc)
            for r in [i[0] for i in self.piece_loc]:
                if '#' in self.env_map[r][right_barrier + 1]:
                    return

            for i, j in self.piece_loc:
                Erase(i, j)
            for i, j in self.piece_loc:
                Write(i, j+1, '#')

            for n, (i, j) in enumerate(self.piece_loc):
                self.piece_loc[n][1] = j+1

        elif k == ord('r'):
            self.Rotate_Piece(self.piece_style)

        elif k == ord('q'):
            self.Quit_Game('quit')



    def Rotate_Piece(self, piece_style):
        
        def Write(row, col, piece):
            self.stdscr.addstr(row, col, piece)

        def Erase(row, col):
            self.stdscr.addstr(row, col, ' ')



        if self.piece_style == 'a':

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




        elif self.piece_style == 'b':

            if (self.piece_rot == False) and (self.piece_rot_setting == None):
                for i, j in self.piece_loc:
                    Erase(i, j)

                left_col = min(i[1] for i in self.piece_loc)
                lower_row = max([i[0] for i in self.piece_loc])
                upper_row = lower_row - 1

                for n, (i, j) in enumerate(self.piece_loc):
                    if i == lower_row and j == left_col:
                        self.piece_loc[n] = [i - 1, j + 1]
                    elif i == lower_row and (j == left_col + 1):
                        pass
                    elif i == lower_row and (j == left_col + 2):
                        self.piece_loc[n] = [i + 1, j - 1]
                    elif i == upper_row:
                        self.piece_loc[n] = [i + 1, j + 1]

                for i, j in self.piece_loc:
                        Write(i, j, '#')

                self.piece_rot = True
                self.piece_rot_setting = 1

            elif (self.piece_rot == True) and (self.piece_rot_setting == 1):
                for i, j in self.piece_loc:
                    Erase(i, j)

                upper_row = min(i[0] for i in self.piece_loc)
                left_col = min([i[1] for i in self.piece_loc])
                right_col = left_col + 1

                for n, (i, j) in enumerate(self.piece_loc):
                    if i == upper_row and j == left_col:
                        self.piece_loc[n] = [i + 1, j + 1]
                    elif (i == upper_row + 1) and (j == left_col):
                        pass
                    elif (i == upper_row + 2) and (j == left_col):
                        self.piece_loc[n] = [i - 1, j - 1]
                    elif j == right_col:
                        self.piece_loc[n] = [i + 1, j - 1]

                for i, j in self.piece_loc:
                        Write(i, j, '#')

                self.piece_rot_setting = 2


            elif (self.piece_rot == True) and (self.piece_rot_setting == 2):
                for i, j in self.piece_loc:
                    Erase(i, j)

                upper_row = min(i[0] for i in self.piece_loc)
                left_col = min([i[1] for i in self.piece_loc])
                lower_row = upper_row + 1

                for n, (i, j) in enumerate(self.piece_loc):
                    if i == upper_row and j == left_col:
                        self.piece_loc[n] = [i - 1, j + 1]
                    elif (i == upper_row) and (j == left_col + 1):
                        pass
                    elif (i == upper_row) and (j == left_col + 2):
                        self.piece_loc[n] = [i + 1, j - 1]
                    elif i == lower_row:
                        self.piece_loc[n] = [i - 1, j - 1]

                for i, j in self.piece_loc:
                        Write(i, j, '#')

                self.piece_rot_setting = 3


            elif (self.piece_rot == True) and (self.piece_rot_setting == 3):
                for i, j in self.piece_loc:
                    Erase(i, j)

                right_col = max(i[1] for i in self.piece_loc)
                upper_row = min([i[0] for i in self.piece_loc])
                left_col = right_col - 1

                for n, (i, j) in enumerate(self.piece_loc):
                    if i == upper_row and j == right_col:
                        self.piece_loc[n] = [i + 1, j + 1]
                    elif (i == upper_row + 1) and (j == right_col):
                        pass
                    elif (i == upper_row + 2) and (j == right_col):
                        self.piece_loc[n] = [i - 1, j - 1]
                    elif j == left_col:
                        self.piece_loc[n] = [i - 1, j + 1]

                for i, j in self.piece_loc:
                        Write(i, j, '#')

                self.piece_rot = False
                self.piece_rot_setting = None
                

        elif self.piece_style == 'c':
            pass



    def Write_Piece_To_Board(self):
        for p0, p1 in self.piece_loc:
            self.env_map[p0][p1] = '#'


    def Check_Advance_Game(self):
        lowest_row = max([x[0] for x in self.piece_loc])
        row_diff_from_bottom = (self.blen-1) - lowest_row
        if all(p == '#' for p in self.env_map[lowest_row]):
            self.Finish_Row_Animation(lowest_row)
            blank_row = list(['#'] + [' ' for _ in range(self.bwidth-1)])
            if row_diff_from_bottom > 0:
                self.env_map = list([blank_row] + self.env_map[:lowest_row] + self.env_map[lowest_row + 1:])
            else:
                self.env_map = list([blank_row] + self.env_map[:-1])
            self.Redraw_Board()

    def Finish_Row_Animation(self, row):

        def Flicker(sleep_time):
            for col in range(1, self.bwidth):
                self.stdscr.addstr(row, col, '=')
           
            self.stdscr.refresh() 
            time.sleep(sleep_time)
            
            for col in range(1, self.bwidth):
                self.stdscr.addstr(row, col, ' ')

            self.stdscr.refresh() 
            time.sleep(sleep_time)

        sleep_time = 0.2
        Flicker(sleep_time)
        Flicker(sleep_time)


    
    def Redraw_Board(self):
        for row in range(self.blen):
            for col in range(1, self.bwidth):
                self.stdscr.addstr(row, col, self.env_map[row][col])

    def Check_End_Of_Game(self):
        for i, j in self.piece_loc:
            if any(p == '#' for p in self.env_map[i+1][j]):
                self.Quit_Game('lose')
    
    def Quit_Game(self, cond):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

        if cond == 'lose':
            self.Write_Piece_To_Board()
            os.system('clear')
            print("You Lost! Here's the Board you lost on: ")
            sys.exit(np.matrix(self.env_map))
        
        elif cond == 'quit':
            os.system('clear')
            sys.exit("Quit game.")







def main():


    diff_dict = {1: 2.0,
                 2: 1.5,
                 3: 1.0,
                 4: 0.5}

    print("What difficulty would you like to play on?")
    print("PRESS 'ENTER' AFTER MAKING YOUR CHOICE")
    print("1: Easy", "2: Medium", "3: Hard", "4: Very Hard")

    choice = input()
    wait_time = diff_dict[int(choice)]

    b = Board(14, 18)

    b.stdscr.timeout(0) # enables automatic drop of piece after 1 second
    k = b.stdscr.getch()
    while True:
        a = time.time()
        while time.time() - a < wait_time:
            b.Move_Piece(k)
            b.stdscr.refresh()
            k = b.stdscr.getch()
        b.Move_Piece(curses.KEY_DOWN)
        b.stdscr.refresh()
        k = b.stdscr.getch()

# Driver
main()