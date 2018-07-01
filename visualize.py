from drawnow import *

##### GLOBAL VARIABLES
plotRange_x = 50
plotRange_y = 20

def applyPlotStyle():
    plt.grid(True)
    plt.xlim(0,plotRange_x)
    plt.ylim(-1 * plotRange_y, plotRange_y)
    #plt.xlabel('Time')
    plt.ylabel('Acceleration (mG)')

def makePlot():
    plt.subplot(2,2,1)
    applyPlotStyle()
    plt.title('Acceleration x')
    plt.plot(ax, 'ro-', label='')

    plt.subplot(2,2,2)
    plt.ylabel('Acceleration (mG)')
    applyPlotStyle()
    plt.title('Acceleration y')
    plt.plot(ay, 'bo-', label='Acceleration y')


    plt.subplot(2,2,3)
    applyPlotStyle()
    plt.title('Acceleration z')
    plt.plot(az, 'go-', label='Acceleration z')


# Interface function
def drawGraphs(_ax, _ay, _az):
    global ax
    global ay
    global az

    ax = _ax
    ay = _ay
    az = _az

    drawnow(makePlot)
