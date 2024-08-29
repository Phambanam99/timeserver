import serial
import serial.tools.list_ports

def find_baud_rate(port):
    baud_rates = [4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]
    for baud_rate in baud_rates:
        try:
            ser = serial.Serial(port, baud_rate, timeout=1)
            ser.write(b'ping\n')  # Gửi lệnh mẫu tới thiết bị
            response = ser.readline()
            ser.close()
            if response:
                print(f"Found valid baud rate: {baud_rate}")
                return baud_rate
        except:
            pass
    print("No valid baud rate found.")
    return None

# Danh sách các cổng nối tiếp có sẵn
def find_port_baud():
    port_bauds = []
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        print(f"Checking port: {port.device}")
        baud_rate = find_baud_rate(port.device)
        if baud_rate:
            port_bauds.append({"port": port.device, "baud": baud_rate})
    return port_bauds
print(find_port_baud())