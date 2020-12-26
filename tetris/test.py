a = [[1],[2],[3],[4],[5],[6],[7],[8]]

a

lowest_row = 4
blank_row = ['']

list([blank_row] + a[:lowest_row] + a[lowest_row + 1:])

a[:4]
