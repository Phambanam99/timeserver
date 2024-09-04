import serial
import time

# Configure the serial port
serial_port = '/dev/ttyS0'  # For GPIO pins 14 (TXD) and 15 (RXD)
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate, timeout=1)

def read_gps_data():
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('ascii', errors='replace')
            print(line)
            if line.startswith('$GNRMC'):
                parts = line.split(',')
                if len(parts) > 1 and parts[1] == 'A':
                    time_str = parts[1]
                    date_str = parts[9]
                    return time_str, date_str
        time.sleep(1)

try:
    while True:
        time_str, date_str = read_gps_data()
        if time_str and date_str:
            print(f"Time: {time_str} Date: {date_str}")
        time.sleep(1)
except KeyboardInterrupt:
    print("Program interrupted")
finally:
    ser.close()
