#
# display_control_server.py - This code runs on the Raspberry Pi and
# coordinates serial communication, state management, LCD updates, LED
# updates, time display, error handling, and graceful system cleanup.
# Hardware operations are delegated to HardwareManager.
#
#------------------------------------------------------------------
# Change History
#------------------------------------------------------------------
# Version   |   Description
#------------------------------------------------------------------
#    1          Initial Enhanced Development
#------------------------------------------------------------------

import logging
import threading

from config import (
    BAUD_RATE,
    DEFAULT_STATE,
    MAIN_LOOP_DELAY,
    SERVER_SERIAL_PORT,
    SERVER_TIMEOUT,
)
from hardware_manager import HardwareManager
from serial_manager import SerialManager
from state_manager import StateManager


def normalize_command(command: str) -> str:
    # Normalizes received state names while preserving internal spaces.
    return " ".join(word.capitalize() for word in command.strip().split())


def update_clock(hardware_manager: HardwareManager,
                 stop_event: threading.Event) -> None:
    # Updates the LCD time independently until shutdown is requested.
    while not stop_event.is_set():
        try:
            hardware_manager.update_time()
        except Exception:
            logging.exception("Unable to update the LCD time.")
            stop_event.set()
            break

        # Waits for the configured delay but exits early during shutdown.
        stop_event.wait(MAIN_LOOP_DELAY)


def run_server() -> None:
    # Runs the Raspberry Pi state display server until shutdown.
    serial_manager = None
    hardware_manager = None
    stop_event = threading.Event()
    clock_thread = None

    try:
        serial_manager = SerialManager(
            port=SERVER_SERIAL_PORT,
            baud_rate=BAUD_RATE,
            timeout=SERVER_TIMEOUT,
        )
        hardware_manager = HardwareManager()
        state_manager = StateManager(DEFAULT_STATE)

        hardware_manager.initialize()
        hardware_manager.display_startup()
        hardware_manager.apply_state(state_manager.current_state)
        hardware_manager.update_time()

        # The clock thread updates the first LCD line independently.
        clock_thread = threading.Thread(
            target=update_clock,
            args=(hardware_manager, stop_event),
            name="LCDClockThread",
        )
        clock_thread.start()

        running = True

        while running:
            command = serial_manager.read_command()

            if command:
                normalized_command = normalize_command(command)

                if normalized_command == "Shutdown":
                    running = False

                elif state_manager.is_valid_state(normalized_command):
                    state_changed = state_manager.transition_to(normalized_command)

                    if state_changed:
                        hardware_manager.apply_state(
                            state_manager.current_state
                        )
                    else:
                        logging.info(
                            "No state change needed. Current state: %s",
                            state_manager.current_state,
                        )

                else:
                    logging.warning(
                        "Rejected invalid command: %r",
                        command,
                    )

    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received. Shutting down.")

    except Exception:
        logging.exception("Unexpected server failure.")

    finally:
        # Stops and joins the clock thread before shutdown LCD writes begin.
        stop_event.set()

        if clock_thread is not None and clock_thread.is_alive():
            clock_thread.join()

        if hardware_manager is not None:
            try:
                hardware_manager.display_shutdown()
            except Exception:
                logging.exception("Unable to display shutdown message.")
            finally:
                try:
                    hardware_manager.cleanup()
                except Exception:
                    logging.exception("Unable to fully clean up hardware.")

        if serial_manager is not None:
            try:
                serial_manager.close()
            except Exception:
                logging.exception("Unable to close serial connection.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
    )
    run_server()
