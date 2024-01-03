from copy import deepcopy
from time import sleep

class Sudoku:
    
    possibilities = None
    t = []
    depth = None
    
    def __init__(self, t, depth) -> None:
        self.t = t
        self.possibilities = self.check_init()
        self.depth = depth
        print(f"=========== NEW ITERATION D:{self.depth} ================")
    
    def check_counts(self, counts):
        """Converts list of nine _int_ where 0 no possibility and 1 where index + 1 means possible number into tuplet of possible numbers

        Args:
            counts (_list_): list of nine _int_

        Returns:
            _tuple_: Tuple of possible numbers
        """
        every = 0
        exists = ()
        # [0,0,0,0,0,0,1,0,0]
        for i, c in enumerate(counts):
            if c > 1:
                return False
            elif c == 1:
                every += 1
            else:
                exists += (i + 1,) 

        if every == 9:
            return True
        else:
            return exists
        
    def check_vertical(self, x):
        """Check possibilities for single column

        Args:
            x (_int_): x coordinate

        Returns:
            _tuplet_: Tuple of possible numbers 
        """
        counts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(9):
            # print(i)
            cell = self.t[i][x]
            if cell > 0 and cell < 10:
                # print(cell)
                counts[cell - 1] += 1
        # print(counts)
        return self.check_counts(counts)
    
    def check_horizontal(self, y):
        """Check possibilities for single row

        Args:
            y (_int_): y coordinate

        Returns:
            _tuplet_: Tuple of possible numbers
        """
        counts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(9):
            # print(i)
            cell = self.t[y][i]
            if cell > 0 and cell < 10:
                # print(cell)
                counts[cell - 1] += 1
        return self.check_counts(counts)
    
    def check_square(self, x, y):
        """Check possibilities for single square

        Args:
            x (_int_): x coordinate
            y (_int_): y coordinate

        Returns:
            _tuplet_: Tuple of possible numbers 
        """
        sx = x // 3 * 3
        sy = y // 3 * 3
        counts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for y in range(sy, sy + 3):
            for x in range(sx, sx + 3):
                cell = self.t[y][x]
                if cell > 0 and cell < 10:
                    # print(cell)
                    counts[cell - 1] += 1
        # print(counts)
        return self.check_counts(counts)
    
    def combine(self, vertical, horizontal, square):
        """Combines vertical, horizontal and square possibilities into possiblities for single field

        Args:
            vertical (_tuple_): vertical possibilities
            horizontal (_tuple_): horizontal possibilities
            square (_tuple_): square possibilities

        Returns:
            _tuple_: Possibilities for single field
        """
        res = []
        for i in range(1, 10):
            t = 0
            if vertical.count(i):
                t += 1
            if horizontal.count(i):
                t += 1
            if square.count(i):
                t += 1
            if t == 3:
               res.append(i)
        return tuple(res) 
    
    def check_init(self):
        """Finds possibilieties for every field in sudoku

        Returns:
            _list_: List of possibilities for every field
        """
        vertical = []
        horizontal = []
        square = []
        
        # vertical possibilities
        for x in range(9):
            vertical.append(self.check_vertical(x))
        
        # horizontal possibilities
        for y in range(9):
            horizontal.append(self.check_horizontal(y))
        
        # square possibilities
        for y in range(0, 9, 3):
            square.append([])
            for x in range(0, 9, 3):
                square[-1].append(self.check_square(x, y))
        
        # check possibilities for every square, by combining information from horizontal, vertical and square
        res = []
        for y in range(9):
            res.append([])
            for x in range(9):
                if self.t[y][x] == 0:
                    v = vertical[x]
                    h = horizontal[y]
                    s = square[y // 3][x // 3]
                    res[-1].append(self.combine(v, h, s))
                else:
                    res[-1].append(None)
                
        return res
    
    def print_possibilities(self):
        """Prints possibilities for every field
        """
        for y in range(9):
            print(f"Row {y}")
            for x in range(9):
                print(f"y={y} x={x} {self.t[y][x]}: pos={self.possibilities[y][x]}")
                
    def find(self):
        """Finds the smallest amount of possibilities

        Returns:
            tuple(x, y): coordinates of smallest possibilities
            True: if sudoku is solved
        """
        coords = None
        possibilities = 9
        for y in range(9):
            for x in range(9):
                cell = self.possibilities[y][x]
                if cell != None:
                    length = len(cell)
                    if length < possibilities and length > 0:
                        coords = (x, y)
                        possibilities = length
        
        if coords != None:
            return coords
        else:
            return False
                    
    
    def remove_possibilities(self, x, y, num):
        """Remove possibility from vertical, horizontal lines and squares for provided coordinates and number which has to be remove

        Args:
            x (_int_): x coordinate
            y (_int_): y coordinate_
            num (_int_): number to remove from possibilities
        """
        
        self.t[y][x] = num
        self.possibilities[y][x] = None
        
        for i in range(9):
            # remove vertical
            cell = self.possibilities[i][x]
            if cell != None:
                cell = list(cell)
                if cell.count(num):
                    cell.remove(num)
                    self.possibilities[i][x] = tuple(cell)
            
            # remove horizontal
            cell = self.possibilities[y][i]
            if cell != None:
                cell = list(cell)
                if cell.count(num):
                    cell.remove(num)
                    self.possibilities[y][i] = tuple(cell)
                
        # remove square
        sy = y // 3 * 3
        sx = x // 3 * 3
        for y in range(sy, sy + 3):
            for x in range(sx, sx + 3):
                cell = self.possibilities[y][x]
                if cell != None:
                    cell = list(cell)    
                    if cell.count(num):
                        cell.remove(num)
                        self.possibilities[y][x] = tuple(cell)
        
    def verify(self):
        """Checks if any zero occurs in self.t

        Returns:
            _bool_: False if there is any zero in self.t or True if there is no zeros
        """
        for y in range(9):
            for x in range(9):
                if self.t[y][x] == 0:
                    return False 
        return True
        
    def solve(self):
        """Solves sudoku

        Returns:
            _list_: Returns solved sudoku
        """
        while True:
            coords = self.find()
            if not coords:
                # if there is no more possiblities and verify return False that means sudoku is wrongly solved
                if self.verify():
                    return self.t
                else:
                    return False
            else:
                x, y = coords
                length = len(self.possibilities[y][x])
                
                # if there is only one possible number just remove it and put the number at this coords
                if length == 1:
                    num = self.possibilities[y][x][0]
                    self.remove_possibilities(x, y, num)
                
                # if there is more than one possible number do reccurency for all possibilities
                else:

                    for i in range(length):

                        t = deepcopy(self.t)
                        t[y][x] = self.possibilities[y][x][i]                        
                        s = Sudoku(t, self.depth + 1)
                        r = s.solve()
                        del s
                        if r:
                            return r
                        
                    return False
                
