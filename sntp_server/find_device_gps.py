import serial
import serial.tools.list_ports

def find_used_ports_and_baudrates(possible_baudrates=[9600, 115200, 38400, 4800]):  # Added 4800
    """Finds used COM ports and attempts to identify their baud rates."""

    used_ports_info = []

    for port in serial.tools.list_ports.comports():
        print(port)
        try:
            for baudrate in possible_baudrates:
                try:
                    with serial.Serial(port.device, baudrate, timeout=1) as ser:
                        # Send a command or query (adjust for your device)
                        ser.write(b"AT\r\n")  
                        response = ser.readline().decode().strip()
                        print(ser.readline())
                        # Check for a valid response (adjust for your device)
                        if "OK" in response:
                            used_ports_info.append((port.device, baudrate))
                            break  # Stop trying other baud rates for this port

                except serial.SerialException:
                    pass  # Ignore errors and continue trying other baud rates

        except serial.SerialException:
            pass  # Ignore errors if the port is in use by another process

    return used_ports_info

if __name__ == "__main__":
    used_ports_and_baudrates = find_used_ports_and_baudrates()

    if used_ports_and_baudrates:
        print("Used COM ports and their identified baud rates:")
        for port, baudrate in used_ports_and_baudrates:
            print(f"  - Port: {port}, Baud Rate: {baudrate}")
    else:
        print("No used COM ports found.")