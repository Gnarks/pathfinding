import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors


neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))
colors_list = ["white","black","green","red","cyan"]
cmap = colors.ListedColormap(colors_list)
bounds = [0,1,2,3,4,5]
norm = colors.BoundaryNorm(bounds, cmap.N)
EMPTY, WALL,CAN,CANT,SPECIAL = 0,1,2,3,4

nx,ny = 10,10


X = np.zeros((nx,ny))

fig, ax = plt.subplots()
im = plt.imshow(X,cmap,norm=norm)

def onclick(event):
    """
    on the first click draws the start then end then walls
    """
    print(event.button)
    if onclick.clicked<2:
        X[round(event.ydata), round(event.xdata)] = SPECIAL
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
    if X[round(event.ydata), round(event.xdata)] != SPECIAL:
        if event.button ==  1:
            X[round(event.ydata), round(event.xdata)] = WALL
        elif event.button == 3:
            X[round(event.ydata), round(event.xdata)] = EMPTY

#handling events to draw the start, end and after both are drawn draw walls
pressed_cid = fig.canvas.mpl_connect('button_press_event', onclick)
# draws walls when the a button is pressed and 
drag_cid = fig.canvas.mpl_connect('motion_notify_event', drag_draw)

def update(i):
    im.set_data(X)


delay = 10
anim = animation.FuncAnimation(fig,update,interval=delay,frames= 200)


plt.show()