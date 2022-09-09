import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors
from math import sqrt


class Tile():
    def __init__(self,position,g_cost,h_cost,parent=None):
        self.position = position
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost+h_cost
        self.parent = parent
        self.x = position[0]
        self.y =[position[1]]



def step(X :np.ndarray):
    """
    function that'll make one step toward the most promising case
    inspired by : https://www.youtube.com/watch?v=-L-WgKMFuhE&ab_channel=SebastianLague
    """
    global cur_pos,start,end
    X1 = X

    best = open[0]
    for free in open:
        if free.position == end or best.f_cost > free.f_cost or (best.f_cost == free.f_cost and best.h_cost > free.h_cost):
            best = free
            if best.position == end:
                parent = best.parent
                while parent:
                    X1[parent.position] = SPECIAL
                    parent = parent.parent
                return X1
    
    
    open.remove(best)
    closed.append(best)
    closed_pos.append(best.position)
    cur_pos = best.position

    for dx,dy in neighbourhood:
        ngb_pos = (cur_pos[0]+dx,cur_pos[1]+dy)

        if X[ngb_pos] != WALL and not closed_pos.__contains__(ngb_pos):
            g = best.g_cost + 14 if abs(dx) +abs(dy) == 2 else best.g_cost + 10
            h = round(sqrt((end[0]-ngb_pos[0])**2 + (end[1]-ngb_pos[1])**2)*10)
            if open_tiles[ngb_pos[0]][ngb_pos[1]] == 0:
                neighbour =Tile(ngb_pos,g,h,best)
                open.append(neighbour)
                open_tiles[ngb_pos[0]][ngb_pos[1]] = neighbour
            elif open_tiles[ngb_pos[0]][ngb_pos[1]].g_cost > g:
                neighbour =Tile(ngb_pos,g,h,best)
                open_tiles[ngb_pos[0]][ngb_pos[1]] = neighbour

    for tile in closed:
        if X1[tile.position] != SPECIAL:
            X1[tile.position] = CANT
    
    for tile in open:
        if X1[tile.position] != SPECIAL and X1[tile.position] != WALL and X1[tile.position]!=CANT:
            X1[tile.position] = CAN

    return X1

neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))
colors_list = ["white","black","green","red","cyan"]
cmap = colors.ListedColormap(colors_list)
bounds = [0,1,2,3,4,5]
norm = colors.BoundaryNorm(bounds, cmap.N)
EMPTY, WALL,CAN,CANT,SPECIAL = 0,1,2,3,4

nx,ny = 21,21

X = np.ones((nx,ny))
X[1:nx-1,1:ny-1] = EMPTY
fig, ax = plt.subplots()
im = plt.imshow(X,cmap,norm=norm)
cur_pos,start,end = (0,0),(0,0),(0,0)
open=[]
closed=[]
open_tiles = np.zeros((nx,ny),dtype=Tile)
closed_pos= []
go = False

def onclick(event):
    """
    on the first click draws the start then end then walls
    """
    global cur_pos,start,end
    if event.inaxes and X[round(event.ydata), round(event.xdata)] != SPECIAL:
        if onclick.clicked<2:
            X[round(event.ydata), round(event.xdata)] = SPECIAL
            if onclick.clicked == 0:
                start = (round(event.ydata), round(event.xdata))
            else:
                end = (round(event.ydata), round(event.xdata))
                open.append(Tile(start,0,round(sqrt((end[0]-start[0])**2 + (end[1]-start[1])**2)*10)))
        else:
            X[round(event.ydata), round(event.xdata)] = WALL
        onclick.clicked +=1
        im.set_data(X)
# count the number of clicks to decide in the function if a start/end/wall should be drawn 
onclick.clicked = 0

def drag_draw(event):
    """
    draw walls when the button if pressed and the mouse is moving
    """
    #verify if the block we're trying to draw on isn't the start or the end
    if event.inaxes:
        if X[round(event.ydata), round(event.xdata)] != SPECIAL:
            if event.button ==  1:
                X[round(event.ydata), round(event.xdata)] = WALL
            elif event.button == 3:
                X[round(event.ydata), round(event.xdata)] = EMPTY

def key_pressed(event):
    global go
    if event.key == " " and onclick.clicked>=2:
        #update.X = step(update.X)
        go = True
        
#handling events to draw the start, end and after both are drawn draw walls
pressed_cid = fig.canvas.mpl_connect('button_press_event', onclick)
# draws walls when the a button is pressed and 
drag_cid = fig.canvas.mpl_connect('motion_notify_event', drag_draw)

key_cid = fig.canvas.mpl_connect("key_press_event",key_pressed)

def update(i):
    global go
    #if onclick.clicked>=2:
    if go :
        update.X = step(update.X)
    im.set_data(update.X)
update.X = X

delay = 40
anim = animation.FuncAnimation(fig,update,interval=delay,frames= 200)
plt.show()