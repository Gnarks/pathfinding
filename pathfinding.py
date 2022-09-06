import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors


def step(X :np.ndarray):
    """
    function that'll make one step toward the most promising case
    https://www.youtube.com/watch?v=-L-WgKMFuhE&ab_channel=SebastianLague
    """
    global cur_pos,start,end
    X1 = X
    
    for dx,dy in neighbourhood:
        print(cur_pos[0]+dx,cur_pos[1]+dy)
        if X1[cur_pos[0]+dx,cur_pos[1]+dy] != WALL and X1[cur_pos[0]+dx,cur_pos[1]+dy] != SPECIAL:
            X1[cur_pos[0]+dx,cur_pos[1]+dy] = CAN
    X1[cur_pos] = CANT
    cur_pos = (cur_pos[0]+1,cur_pos[1]+1)
    return X1


neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))
colors_list = ["white","black","green","red","cyan"]
cmap = colors.ListedColormap(colors_list)
bounds = [0,1,2,3,4,5]
norm = colors.BoundaryNorm(bounds, cmap.N)
EMPTY, WALL,CAN,CANT,SPECIAL = 0,1,2,3,4

nx,ny = 11,11

X = np.ones((nx,ny))
X[1:nx-1,1:ny-1] = 0
fig, ax = plt.subplots()
im = plt.imshow(X,cmap,norm=norm)
cur_pos,start,end = (0,0),(0,0),(0,0)


def onclick(event):
    """
    on the first click draws the start then end then walls
    """
    global cur_pos,start,end
    if event.inaxes:
        if onclick.clicked<2:
            X[round(event.ydata), round(event.xdata)] = SPECIAL
            if onclick.clicked == 0:
                start = (round(event.ydata), round(event.xdata))
                cur_pos = start
            else:
                end = (round(event.ydata), round(event.xdata))
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
    if event.key == " " and onclick.clicked>=2:
        update.X = step(update.X)

#handling events to draw the start, end and after both are drawn draw walls
pressed_cid = fig.canvas.mpl_connect('button_press_event', onclick)
# draws walls when the a button is pressed and 
drag_cid = fig.canvas.mpl_connect('motion_notify_event', drag_draw)

key_cid = fig.canvas.mpl_connect("key_press_event",key_pressed)

def update(i):
    """
    if onclick.clicked>=2:
        update.X = step(update.X)"""
    im.set_data(update.X)
update.X = X

delay = 10
anim = animation.FuncAnimation(fig,update,interval=delay,frames= 200)
plt.show()