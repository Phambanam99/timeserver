import socket
import time
def get_time_from_server(host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    server_time = client_socket.recv(1024).decode('utf-8')
    client_socket.close()
    return server_time

if __name__ == "__main__":
    while True:
        server_time = get_time_from_server()
        print(f"Received time from server: {server_time}")
        time.sleep(5)  # Wait for 5 seconds before the next request