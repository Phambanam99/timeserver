import serial
import serial.tools.list_ports
import os
def find_used_ports_and_baudrates(possible_baudrates=[9600, 115200, 38400, 4800]):  # Added 4800
    """Finds used COM ports and attempts to identify their baud rates."""
   # Directory containing tty devices
    dev_directory = '/dev/'
    # List all files in /dev/
    all_files = os.listdir(dev_directory)
    # Filter files that start with 'tty'
    tty_devices = [f for f in all_files if f.startswith('ttyS0')]
    used_ports_info = []
    for tty_device in tty_devices:
        tty_device = "/dev/" +  tty_device
        for baudrate in possible_baudrates:
            try:
                with serial.Serial(tty_device, baudrate, timeout=1) as ser:
                    # Send a command or query (adjust for your device)
                    ser.write(b'ping\n')  # Gửi lệnh mẫu tới thiết bị
                    response = ser.readline()
                    ser.close()
                    # Check for a valid response (adjust for your device)
                    if  response:
                        used_ports_info.append((tty_device, baudrate))
                        break  # Stop trying other baud rates for this port

            except serial.SerialException:
                pass  # Ignore errors and continue trying other baud rates
    return used_ports_info

if __name__ == "__main__":
    used_ports_and_baudrates = find_used_ports_and_baudrates()
    
    if used_ports_and_baudrates:
        print("Used COM ports and their identified baud rates:")
        for port, baudrate in used_ports_and_baudrates:
            print(f"  - Port: {port}, Baud Rate: {baudrate}")
    else:
        print("No used COM ports found.")
