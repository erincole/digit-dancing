import time
import serial
import matplotlib.pyplot as plt
import array
import matplotlib.animation as animation
from math import cos, sin
import datetime as dt

ardi = serial.Serial('COM4', 9600, timeout=1) # create arduino
num_l = 0
num_r = 0

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
thetas = [] # define list to hold input vals
betas = [] # define list to hold input vals
r1s = []
r2s = []
r3s = []
xs = []
num_l = None
num_r = None

def animate(i, thetas, r1, betas, r2, r3):
    global r1s, r2s, r3s, xs, num_l, num_r

    line = ardi.readline().decode('UTF-8') # read from arduino
    # extract integer value from arduino serial:
    if line[:2] == 'L:':
        num_l = int(line[2:])
    elif line[:2] == 'R:':
        num_r = int(line[2:])

    # add to x and y lists
    if num_l is not None and num_r is not None:
        r1s.append(1-cos(num_l)*sin(3*num_l)) # define r1 eqn
        r2s.append(0.5*cos(3*num_r)) # define r2 eqn
        r3s.append(0.72+2*cos(num_l)) # define r3 eqn
        thetas.append(num_l) # add to list of theta values
        betas.append(num_r) # add to list of beta values

        num_l = None
        num_r = None

        #limt lists to 20 items
        thetas = thetas[-20:]
        betas = betas[-20:]
        r1s = r1s[-20:]
        r2s = r2s[-20:]
        r3s = r3s[-20:]

        #draw lists
        ax.clear()
        ax.plot(thetas, r1s)
        ax.plot(betas, r2s)
        ax.plot(thetas, r3s)

while True:
    #format plot
    plt.title('attempt @ polar-beardom')
    annie = animation.FuncAnimation(fig, animate, fargs=(thetas, r1s, betas, r2s, r3s), interval = 50)
    plt.tick_params(
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        left=False,
        labelbottom=False,  # labels along the bottom edge are off
        labelleft=False)
    ax.set_facecolor('#000000')
    fig.set_facecolor('#000000')
    plt.show()