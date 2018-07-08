import serial as sr
import numpy as np
import visualize as vis

##### GLOBAL VARIABLES
port = '/dev/ttyUSB0'
baud = 9600

##### READINGS LIST
ax_readings = []
ay_readings = []
az_readings = []

if __name__ == '__main__':
    serial = sr.Serial(port, baud)

    # Counter for the graph
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

            vis.drawGraphs(ax_readings, ay_readings, ay_readings)

            count += 1
            if(count > 50):
                ax_readings.pop(0)
                ay_readings.pop(0)
                az_readings.pop(0)
