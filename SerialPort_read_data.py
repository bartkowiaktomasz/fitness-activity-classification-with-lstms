import serial as sr
import numpy as np
#import Visualization as visualize
from drawnow import *


##### GLOBAL VARIABLES
port = '/dev/ttyUSB0'
baud = 9600

plotRange_x = 50
plotRange_y = 2000

##### READINGS LIST
ax_readings = []
ay_readings = []
az_readings = []

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
    plt.plot(ax_readings, 'ro-', label='')

    plt.subplot(2,2,2)
    plt.ylabel('Acceleration (mG)')
    applyPlotStyle()
    plt.title('Acceleration y')
    plt.plot(ay_readings, 'bo-', label='Acceleration y')


    plt.subplot(2,2,3)
    applyPlotStyle()
    plt.title('Acceleration z')
    plt.plot(az_readings, 'go-', label='Acceleration z')

if __name__ == '__main__':
    serial = sr.Serial(port, baud)

    count = 0
    while True:
        line = serial.readline()

        # Convert byte to string
        measurements = str(line, 'utf-8')

        # Strip of carriage return and new line
        accelerations = measurements.rstrip('\r\n').split(' ')

        # If the list contains 9 numbers (3x acc, 3x gryo, 3x magneto)
        if(len(accelerations) == 9):
            accelerations = [float(i) for i in accelerations]
            ax = accelerations[0]
            ay = accelerations[1]
            az = accelerations[2]

            gx = accelerations[3]
            gy = accelerations[4]
            gz = accelerations[5]

            mx = accelerations[6]
            my = accelerations[7]
            mz = accelerations[8]

            print(ax, ay, az)
            ax_readings.append(ax)
            ay_readings.append(ay)
            az_readings.append(az)
            # drawnow(makePlot)

            count += 1
            if(count > 50):
                ax_readings.pop(0)
                ay_readings.pop(0)
                az_readings.pop(0)
