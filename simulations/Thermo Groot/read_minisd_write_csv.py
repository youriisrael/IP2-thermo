import serial
import serial.tools.list_ports
import time
import os 
#vraagt naar waar je het bestand wilt opslaan
save_path = os.getcwd()
input_file_name = input("file name: ")




# Zoek automatisch naar de Arduino
def find_arduino():
    ports = serial.tools.list_ports.comports()

    for port in ports:
        print(f"Found: {port.device} - {port.description}")

        if ("Arduino" in (port.description or "") or
                "Arduino" in (port.manufacturer or "")):
            return port.device

    return None


PORT = find_arduino()
BAUD = 115200

if PORT is None:
    print("No Arduino found!")
    raise SystemExit(1)


with serial.Serial(PORT, BAUD, timeout=10) as ser:

    # Allow the Arduino to reset after connecting
    time.sleep(2)

    # Clear any startup messages
    ser.reset_input_buffer()

    # Request the CSV
    print("Waiting for CSV data...")

    ser.write(b'D')

    while True:
        
        
        line = ser.readline()
        print(line)
        if not line:
            raise TimeoutError("Arduino did not respond")

        if line.strip() == b"BEGIN_DATA":
            break

    with open(save_path + rf"\{input_file_name}.csv", "wb") as f:
        while True:
            line = ser.readline()
            print(line)

            if not line:
                raise TimeoutError("CSV transfer timed out")

            if line.strip() == b"END_DATA":
                break

            f.write(line)

print("DATA.CSV saved successfully!")