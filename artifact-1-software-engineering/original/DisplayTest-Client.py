#
# DisplayControl-Client.py - This code runs as the user interface
# for sending commands to the Raspberry Pi server over serial.
# It allows the user to select system states and sends updates
# only when a valid change is made.
#
#------------------------------------------------------------------
# Change History
#------------------------------------------------------------------
# Version   |   Description
#------------------------------------------------------------------
#    1          Initial Development
#------------------------------------------------------------------

# Load serial module
import serial

# Handles shutdown command to server and exits client loop
def shutdownClient():
    ser.write("shutdown\n".encode())
    print("Shutdown command sent.")
    return False


# Menu options for system states
menuOptions = {
    "1": "Running",
    "2": "Idle",
    "3": "Soft Error",
    "4": "Hard Error",
    "5": "Shutdown"
}

# Initialize client-side state
currentState = "Idle"

# Configure serial connection using USB TTL adapter
ser = serial.Serial(
    port="/dev/ttyUSB0",        # USB TTL adapter
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


repeat = True

# handles user input and sends commands
while repeat:
    try:

        # Display current state and menu
        print("\nCurrent State:", currentState)
        print("Set State to:")

        for key, value in menuOptions.items():
            print(f"{key}: {value}")

        validInput = False

        # Loop until valid input is received
        while not validInput:

            userInput = input("Select 1-5: ").strip()

            match userInput:

                # Valid state selections
                case "1" | "2" | "3" | "4":

                    newState = menuOptions[userInput]

                    # Only send if state actually changes
                    if newState != currentState:
                        ser.write((newState + "\n").encode())
                        currentState = newState
                    else:
                        print("No state change needed.")

                    validInput = True

                # Shutdown option
                case "5":
                    repeat = shutdownClient()
                    validInput = True

                # Invalid input
                case _:
                    print("Invalid selection.")

    except KeyboardInterrupt:
        repeat = shutdownClient()