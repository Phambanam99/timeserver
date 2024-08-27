import socket
import struct
import time
from gps import * # Giả sử bạn đã có thư viện GPS phù hợp

# Cấu hình máy chủ NTP
HOST = ''  # Listen on all available interfaces
PORT = 123  # Cổng NTP mặc định

# Khởi tạo đối tượng GPS
gpsd = gps(mode=WATCH_ENABLE) 

def get_gps_time():
    """Lấy thời gian từ tín hiệu GPS"""
    while True:
        report = gpsd.next()
        if report['class'] == 'TPV' and 'time' in report:
            gps_time = report['time']
            return time.mktime(time.strptime(gps_time, "%Y-%m-%dT%H:%M:%S.%fZ"))

def handle_client(client_socket):
    """Xử lý yêu cầu NTP từ client"""
    # Lấy thời gian hiện tại từ GPS
    current_time = get_gps_time()

    # Tạo gói tin NTP để gửi lại cho client
    # (Đơn giản hóa, bạn có thể cần triển khai đầy đủ hơn theo RFC 5905)
    ntp_packet = struct.pack('!12I', 
                             0x1b,  # LI, VN, Mode
                             0, 0, 0, 0, 0, 0, 0, 0,  # Stratum, Poll, Precision, etc.
                             int(current_time),  # Transmit Timestamp (seconds)
                             int((current_time - int(current_time)) * 2**32))  # Transmit Timestamp (fraction)

    # Gửi gói tin NTP cho client
    client_socket.sendto(ntp_packet, client_address)

# Tạo socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print("Máy chủ NTP đang lắng nghe trên cổng", PORT)

while True:
    # Chờ yêu cầu từ client
    data, client_address = server_socket.recvfrom(1024)

    # Xử lý yêu cầu
    handle_client(server_socket)