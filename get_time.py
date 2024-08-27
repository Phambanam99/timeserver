import serial
import pynmea2
# Configure the serial connection (replace 'COM3' with your port if different)
ser = serial.Serial('COM3', 4800, timeout=1)
try:
    while True:
        line = ser.readline().decode('ascii', errors='replace')
        if line.startswith('$GPRMC') or line.startswith('$GPGGA'):
            msg = pynmea2.parse(line)
            gps_time = msg.timestamp
            print(f"GPS Time: {gps_time}")
except serial.SerialException as e:
    print(f"Error: {e}")
except pynmea2.nmea.ChecksumError as e:
    print(f"NMEA checksum error: {e}")
finally:
    ser.close()
