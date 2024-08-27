import serial
import time

# Connect to the GPS device on COM4 at 9600 baud
ser = serial.Serial('COM4', 9600, timeout=1)  # Adjust timeout as needed
# Wait for a valid GPS fix and extract the time
while True:
    line = ser.readline().decode('utf-8').strip()
    print(line)