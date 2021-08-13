import random
import time
import pandas as pd
from IPython.display import clear_output

{
    "editor.fontSize": 40,
    "window.zoomLevel": 1.5,
}


def tableize(df):
    if not isinstance(df, pd.DataFrame):
        return
    df_columns = df.columns.tolist()
    max_len_in_lst = lambda lst: len(sorted(lst, reverse=True, key=len)[0])
    align_center = lambda st, sz: "{0}{1}{0}".format(" " * (1 + (sz - len(st)) // 2), st)[:sz] if len(st) < sz else st
    align_right = lambda st, sz: "{0}{1} ".format(" " * (sz - len(st) - 1), st) if len(st) < sz else st
    max_col_len = max_len_in_lst(df_columns)
    max_val_len_for_col = dict(
        [(col, max_len_in_lst(df.iloc[:, idx].astype('str'))) for idx, col in enumerate(df_columns)])
    col_sizes = dict([(col, 2 + max(max_val_len_for_col.get(col, 0), max_col_len)) for col in df_columns])
    build_hline = lambda row: '+'.join(['-' * col_sizes[col] for col in row]).join(['+', '+'])
    build_data = lambda row, align: "|".join(
        [align(str(val), col_sizes[df_columns[idx]]) for idx, val in enumerate(row)]).join(['|', '|'])
    hline = build_hline(df_columns)
    out = [hline, build_data(df_columns, align_center), hline]
    for _, row in df.iterrows():
        out.append(build_data(row.tolist(), align_right))
    out.append(hline)
    return "\n".join(out)


def solve_grid(grid):
    length = len(grid)
    width = len(grid[0])

    for i in range(0, len(grid)):
        for x in range(0, len(grid[i])):
            if grid[i][x] == "-":
                grid[i][x] = 0
                if x != 0 and grid[i][x - 1] == '#':
                    grid[i][x] += 1
                if i != 0 and grid[i - 1][x] == '#':
                    grid[i][x] += 1
                if x != width - 1 and grid[i][x + 1] == '#':
                    grid[i][x] += 1
                if i != length - 1 and grid[i + 1][x] == '#':
                    grid[i][x] += 1
                if i != 0 and x != 0 and grid[i - 1][x - 1] == '#':
                    grid[i][x] += 1
                if i != 0 and x != width - 1 and grid[i - 1][x + 1] == '#':
                    grid[i][x] += 1
                if i != length - 1 and x != width - 1 and grid[i + 1][x + 1] == '#':
                    grid[i][x] += 1
                if i != length - 1 and x != 0 and grid[i + 1][x - 1] == '#':
                    grid[i][x] += 1
            grid[i][x] = str(grid[i][x])

    return grid


def print_grid(grid):
    print("      ", end="")
    for i in range(0, len(grid)):
        if i >= 9:
            print(i + 1, end="  ")
        else:
            print(i + 1, end="   ")
    print("")
    print("     ", end="")
    for i in range(0, len(grid)):
        print("____", end="")
    print("")
    print("")

    for i in range(0, len(grid)):
        if i > 8:
            print(i + 1, end=" |  ")
        else:
            print(i + 1, end="  |  ")
        for j in range(0, len(grid[i])):
            print(grid[i][j], end="   ")
        if i != len(grid) - 1:
            print("")
            print("   |")
        else:
            print("")
            print("")


def create_grid(length):
    dashlist = []

    for i in range(0, length):
        dashlist.append([])
        for x in range(0, length):
            dashlist[i].append("-")

    return dashlist


def add_mines(minedlist, probability):
    for i in range(0, length):
        for x in range(0, length):
            if random.randint(0, probability) == probability:
                minedlist[i][x] = "#"

    return minedlist


def dig(x, y, solvedgrid, oglist):
    length = len(solvedgrid)
    if solvedgrid[y][x] == "0":
        solvedgrid[y][x] = "x"
        oglist[y][x] = "x"

        if x != 0:
            dig(x - 1, y, solvedgrid, oglist)
        if y != 0:
            dig(x, y - 1, solvedgrid, oglist)
        if x != length - 1:
            dig(x + 1, y, solvedgrid, oglist)
        if y != length - 1:
            dig(x, y + 1, solvedgrid, oglist)
        if y != 0 and x != 0:
            dig(x - 1, y - 1, solvedgrid, oglist)
        if y != 0 and x != length - 1:
            dig(x + 1, y - 1, solvedgrid, oglist)
        if y != length - 1 and x != length - 1:
            dig(x + 1, y + 1, solvedgrid, oglist)
        if y != length - 1 and x != 0:
            dig(x - 1, y + 1, solvedgrid, oglist)
    else:
        oglist[y][x] = solvedgrid[y][x]


def createFinalist(wingrid):
    for i in range(0, len(wingrid)):
        for x in range(0, len(wingrid[i])):
            if wingrid[i][x] == "0":
                wingrid[i][x] = "x"

            if wingrid[i][x] == "#":
                wingrid[i][x] = "-"


def win():
    print("______________________________________________________________________")
    print("")
    print("You win, you are clearly much smarter than a stuti/vihaan! Play again.")
    print("______________________________________________________________________")
    print("")
    endTime = time.time()
    score = int((endTime - startTime) * 100) / 100
    name = input("You have a High Score! What is your name: ")
    print("")

    scores = pd.DataFrame([[level, score, name]])
    scores.to_csv('Minesweeper_High_Scores.csv', mode='a', header=False, index=False)
    Highscores = pd.read_csv("Minesweeper_High_Scores.csv")
    df_sorted = Highscores.sort_values(["Difficulty Level", "Time"], ascending=[False, True])
    print(tableize(df_sorted))
    df_sorted.to_csv("Minesweeper_High_Scores.csv", index=False)


level = input("choose simple, intermediate, or advanced: ")

if level == "simple":
    length = 9
    probability = 8
elif level == "intermediate":
    length = 15
    probability = 7
elif level == "advanced":
    length = 21
    probability = 6

startTime = time.time()
oglist = create_grid(length)
print_grid(oglist)
x = int(input("Enter an x coordinate(starting from the left): "))
x -= 1
y = int(input("Enter an y coordinate(starting from the top): "))
y -= 1

minedlist = create_grid(length)
solvedgrid = solve_grid(add_mines(minedlist, probability))

while solvedgrid[y][x] != "0":
    minedlist = create_grid(length)
    solvedgrid = solve_grid(add_mines(minedlist, probability))

wingrid = []

for i in range(0, len(solvedgrid)):
    wingrid.append([])
    for z in range(0, len(solvedgrid[i])):
        wingrid[i].append(solvedgrid[i][z])

createFinalist(wingrid)

minehit = False

dig(x, y, solvedgrid, oglist)

if oglist == wingrid:
    win()
    minehit = True
else:
    print_grid(oglist)

while minehit == False:
    x = int(input("Enter an x coordinate(starting from the left): "))
    x -= 1
    y = int(input("Enter an y coordinate(starting from the top): "))
    y -= 1

    if solvedgrid[y][x] == "#":
        print("__________________________________________________")
        print("")
        print("Game Over!")
        print("Tough luck, or no brains. Play Again")
        minehit = True

    else:
        dig(x, y, solvedgrid, oglist)
        clear_output(wait=True)
        print_grid(oglist)

    if oglist == wingrid:
        win()
        minehit = True
