'''
//--- TO DO ---//
1. Główne okno z interaktywną siatką przy użyciu pygame.
2. Okno wyboru koordynatów początku i końca przy użyciu tkinter.
3. Algorytm sam w sobie.
4. Wizualizacja algorytmu.
'''

#Imports#
try:
    import pygame
    import sys
    import math
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
    import os
except:
    import install_requirements  # install packages

    import pygame
    import sys
    import math
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
    import os

#---#

screen = pygame.display.set_mode((800, 800))

#class Spot which is literally just a square in a grid with certain features#


class Spot:
    def __init__(self, x, y):
        self.i = x
        self.j = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.obstacle = False
        self.previous = None
        self.closed = False
        self.value = 1
# ---Method which actually draws a rectangle with certain color, position and line thickness. self.i*WIDTH and self.j*HEIGHT are rectangle's coordinates with WIDTH and HEIGHT
#being his dimensions. st is for line thickness---#

    def show(self, color, st):
        if self.closed == False:
            pygame.draw.rect(screen, color, (self.i*WIDTH, self.j*HEIGHT, WIDTH, HEIGHT), st)
            pygame.display.update()
#---Method which handles adding neighboring tiles---#

    def addNeig(self, grid):
        i = self.i
        j = self.j
        if i < cols-1 and grid[self.i + 1][j].obstacle == False:
            self.neighbors.append(grid[self.i + 1][j])
        if i > 0 and grid[self.i - 1][j].obstacle == False:
            self.neighbors.append(grid[self.i - 1][j])
        if j < rows-1 and grid[self.i][j + 1].obstacle == False:
            self.neighbors.append(grid[self.i][j + 1])
        if j > 0 and grid[self.i][j - 1].obstacle == False:
            self.neighbors.append(grid[self.i][j - 1])

#Constants#


red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (130, 125, 125)
cols = 50
rows = 50
WIDTH = 800/cols
HEIGHT = 800/rows
grid = [0 for i in range(cols)]
openSet = []
closedSet = []

#---#
#---Creating a 2D array of 0's, which then will be changed for the sake of Spot class objects---#

for i in range(cols):
    grid[i] = [0 for i in range(rows)]

#---#

#---Filling an array with spots---#

for i in range(cols):
    for j in range(rows):
        grid[i][j] = Spot(i, j)

#---#

#---Temporarly setting a start and end on a grid---#
start = grid[10][5]
end = grid[40][2]
#---#

#---Drawing a grid consisting of white rectangles with black borders---#
for i in range(cols):
    for j in range(rows):
        grid[i][j].show((255, 255, 255), 0)
        grid[i][j].show((0, 0, 0), 1)  # 1 stands for line thickness

#---#

#---Having a problem with borders of the screen, I decided just to fill them with spots with obstacle == True---#
for i in range(0, rows):
    grid[0][i].show(grey, 0)  # Zero stands for filling a rectangle
    grid[0][i].obstacle = True
    grid[cols-1][i].show(grey, 0)
    grid[cols-1][i].obstacle = True
    grid[i][rows-1].show(grey, 0)
    grid[i][rows-1].obstacle = True
    grid[i][0].show(grey, 0)
    grid[i][0].obstacle = True
#---#
#---Functions---#

# Function clicked handles coordinates given by a user which are in format (x,y). It splits the given string in terms of a comma and then
# sets both starting and ending node depending on given coordinates


def clicked():
    global start
    global end
    st = beginBox.get().split(',')
    ed = endingBox.get().split(',')
    start = grid[int(st[0])][int(st[1])]
    end = grid[int(ed[0])][int(ed[1])]
    win.quit()
    win.destroy()
#---#
#---Creating Tkinter submitting window---#


win = Tk()
slabel = Label(win, text='Start (x, y; max = 50)')
beginBox = Entry(win)
elabel = Label(win, text='End (x, y; max = 50)')
endingBox = Entry(win)
zmn = IntVar()
ifpath = ttk.Checkbutton(win, text='Do you want to see steps?', onvalue=1, offvalue=0, variable=zmn)
submit = Button(win, text='Submit', command=clicked)

ifpath.grid(columnspan=2, row=2)
submit.grid(columnspan=2, row=3)
slabel.grid(row=1, pady=3)
endingBox.grid(row=1, column=1, pady=3)
beginBox.grid(row=0, column=1, pady=3)
elabel.grid(row=0, pady=3)

win.update()
mainloop()

pygame.init()
openSet.append(start)

#---#
# Function mpress handles mouse clicks. Depending on which tile we click it changes its obstacle feature to True and changes its color to indicate the diffence
# in obstacle feature.


def mpress(a):
    t = a[0]
    w = a[1]
    xp = t // (800 // cols)
    yp = w // (800 // rows)
    b = grid[xp][yp]
    if b != start and b != end:
        if b.obstacle == False:
            b.obstacle = True
            b.show((0, 0, 0), 0)


#---#
#---pygame loop---#
end.show((255, 8, 127), 0)
start.show((255, 8, 127), 0)

loop = True

while loop:
    ev = pygame.event.get()

    for event in ev:
        pygame.init()
        if event.type == pygame.QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            try:
                position = pygame.mouse.get_pos()
                mpress(position)
            except AttributeError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.type == pygame.K_SPACE:
                loop = False
                break


#---#

for i in range(cols):
    for j in range(rows):
        grid[i][j].addNeig(grid)

# Defining heuristics which is esentially just a carthesian distance


def heuristic(n, e):
    d = math.sqrt((n.i-e.i)**2 + (n.j-e.j)**2)
    return d


#---Initializing pygame code and adding a starting point to the openSet list---#


#---#

# Defining main function
def main():
    end.show((255, 8, 127), 0)
    start.show((255, 8, 127), 0)
    if len(openSet) > 0:
        low = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[low].f:
                low = i

        cur = openSet[low]
        if cur == end:
            print('done', cur.f)
            start.show((255, 8, 127), 0)
            temporary = cur.f
            for i in range(round(cur.f)):
                cur.closed = False
                cur.show((0, 0, 255), 0)
                cur = cur.previous
            end.show((255, 8, 127), 0)

            Tk().wm_withdraw()
            result = messagebox.askokcancel('Algorithm finished', ('Algorithm has finished its work, the shoretest path was:' + str(temporary) + 'Do you want to rerun the program?'))
            if result == True:
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                mb = True
                while mb:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            mb = False
                            break
            pygame.quit()

        openSet.pop(low)
        closedSet.append(cur)

        neighbors = cur.neighbors
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            if neighbor not in closedSet:
                tempG = cur.g + cur.value
                if neighbor in openSet:
                    if neighbor.g > tempG:
                        neighbor.g = tempG
                else:
                    neighbor.g = tempG
                    openSet.append(neighbor)

            neighbor.h = heuristic(neighbor, end)
            neighbor.f = neighbor.g + neighbor.h

            if neighbor.previous == None:
                neighbor.previous = cur
    if zmn.get():
        for i in range(len(openSet)):
            openSet[i].show(green, 0)

        for i in range(len(closedSet)):
            if closedSet[i] != start:
                closedSet[i].show(red, 0)
    cur.closed = True


#
while True:
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        pygame.quit()
    pygame.display.update()
    main()
