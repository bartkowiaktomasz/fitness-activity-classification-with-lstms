import serial as sr

port = '/dev/ttyUSB1'
baud = 9600

serial = sr.Serial(port, baud)

line = []

while True:
    print(serial.readline())
