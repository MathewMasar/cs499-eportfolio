#
# display_control_client.py - This code runs as the user interface for
# sending machine-state commands to the Raspberry Pi server over serial.
# It displays the current state, validates menu selections, avoids
# duplicate state updates, and sends a shutdown command when requested.
#
#------------------------------------------------------------------
# Change History
#------------------------------------------------------------------
# Version   |   Description
#------------------------------------------------------------------
#    1          Initial Enhanced Development
#------------------------------------------------------------------

from config import (
    BAUD_RATE,
    CLIENT_SERIAL_PORT,
    CLIENT_TIMEOUT,
    DEFAULT_STATE,
)
from serial_manager import SerialManager


MENU_OPTIONS = {
    "1": "Running",
    "2": "Idle",
    "3": "Soft Error",
    "4": "Hard Error",
    "5": "Shutdown",
}


def display_menu(current_state: str) -> None:
    #Displays the current state and available menu options
    print("\nCurrent State:", current_state)
    print("Set State to:")

    for key, value in MENU_OPTIONS.items():
        print(f"{key}: {value}")


def get_valid_selection() -> str:
    # Prompts until the user selects a valid menu option.
    while True:
        user_input = input("Select 1-5: ").strip()

        if user_input in MENU_OPTIONS:
            return user_input

        print("Invalid selection.")


def send_shutdown(serial_manager: SerialManager) -> None:
    # Sends the shutdown command to the server
    serial_manager.send_command("Shutdown")
    print("Shutdown command sent.")


def run_client() -> None:
    # Runs the command-line client until shutdown is requested.
    serial_manager = None
    current_state = DEFAULT_STATE
    running = True

    try:
        serial_manager = SerialManager(
            port=CLIENT_SERIAL_PORT,
            baud_rate=BAUD_RATE,
            timeout=CLIENT_TIMEOUT,
        )

        while running:
            display_menu(current_state)
            selection = get_valid_selection()
            new_state = MENU_OPTIONS[selection]

            if new_state == "Shutdown":
                send_shutdown(serial_manager)
                running = False

            elif new_state == current_state:
                print("No state change needed.")

            else:
                serial_manager.send_command(new_state)
                current_state = new_state

    except KeyboardInterrupt:
        if serial_manager is not None:
            try:
                send_shutdown(serial_manager)
            except Exception:
                print("\nUnable to send shutdown command.")
        running = False

    except Exception as error:
        print(f"Client error: {error}")

    finally:
        if serial_manager is not None:
            serial_manager.close()


if __name__ == "__main__":
    run_client()
