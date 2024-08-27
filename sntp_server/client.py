import socket
import struct
import time

def sntp_request(host='127.0.0.1', port=123):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Send an SNTP request (empty message)
    client_socket.sendto(b'\x1b' + 47 * b'\0', (host, port))

    # Receive the response and unpack it
    message, _ = client_socket.recvfrom(48)
    client_socket.close()

    # Unpack the binary response into integers
    unpacked = struct.unpack("!12I", message)

    # Extract the transmit timestamp (seconds and fraction)
    transmit_seconds = unpacked[10]
    print(transmit_seconds)
    transmit_fraction = unpacked[11]
    transmit_timestamp = transmit_seconds + transmit_fraction / 2**32

    # Convert SNTP epoch (1900-01-01) to Unix epoch (1970-01-01)
    epoch = 2208988800
    server_time = transmit_timestamp - epoch

    # Convert to readable time format
    try:
        print(server_time)
        return time.ctime(server_time)
    except ValueError as e:
        print(f"Error converting time: {e}")
        return None

if __name__ == "__main__":
    while True:
        try:
            server_time = sntp_request()
            if server_time:
                print(f"Received time from SNTP server: {server_time}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(5)  # Wait 5 seconds before the next request
