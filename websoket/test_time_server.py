import socket
import serial
import pynmea2

def get_gps_time():
    ser = serial.Serial('COM3', 4800, timeout=1)
    try:
        while True:
            line = ser.readline().decode('ascii', errors='replace')
            if line.startswith('$GPRMC') or line.startswith('$GPGGA'):
                msg = pynmea2.parse(line)
                gps_time = msg.timestamp
                return gps_time
    except serial.SerialException as e:
        print(f"Serial Error: {e}")
    except pynmea2.nmea.ChecksumError as e:
        print(f"NMEA checksum error: {e}")
    finally:
        ser.close()

def start_time_server(host='0.0.0.0', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Time server running on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        gps_time = get_gps_time()
        if gps_time:
            client_socket.sendall(str(gps_time).encode('utf-8'))
        client_socket.close()

if __name__ == "__main__":
    start_time_server()
