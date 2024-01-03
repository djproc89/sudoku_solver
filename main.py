from Load import Load
from Sudoku import Sudoku
from pathlib import Path

path = Path(__file__).parent

def show(t):
    for row in t:
        print("+-+-+-+-+-+-+-+-+-+")
        for cell in row:
            print(f"|{cell}", end="")
        print("|")
    print("+-+-+-+-+-+-+-+-+-+")

f = input("Type file name: ")
t = Load(path / f)
if t:
    s = Sudoku(t, 0)
    show(s.solve())
