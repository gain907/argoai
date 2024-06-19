import serial
import time

def led_control():
    try:
        # ?? ?? ?? (??? ????? ?? ?? ??? ?? ??)
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        time.sleep(2)  # ?????? ?? ??? ?? ?? ??

        while True:
            command = input("Enter '1' to turn ON the LED, '0' to turn OFF the LED, 'q' to quit: ")

            if command == '1' or command == '0':
                ser.write(command.encode())
                print(f"Sent: {command}")

            elif command == 'q':
                print("Exiting...")
                break

            else:
                print("Invalid input. Please enter '1', '0', or 'q'.")

    except serial.SerialException as e:
        print(f"Error: {e}")

    finally:
        ser.close()
        print("Serial port closed.")

if __name__ == "__main__":
    led_control()
