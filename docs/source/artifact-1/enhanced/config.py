#
# config.py - This file stores the shared configuration values used
# by the client and Raspberry Pi server. It centralizes serial settings,
# LCD dimensions, GPIO pin assignments, and timing values so hardware
# and communication settings are not duplicated throughout the project.
#
#------------------------------------------------------------------
# Change History
#------------------------------------------------------------------
# Version   |   Description
#------------------------------------------------------------------
#    1          Initial Enhanced Development
#------------------------------------------------------------------

# Serial communication settings
CLIENT_SERIAL_PORT = "/dev/ttyUSB0"
SERVER_SERIAL_PORT = "/dev/ttyS0"
BAUD_RATE = 115200
CLIENT_TIMEOUT = 1
SERVER_TIMEOUT = 0.1

# LCD settings
LCD_COLUMNS = 16
LCD_ROWS = 2

# GPIO pin assignments using BCM numbering
LED_PINS = {
    "Running": 25,
    "Idle": 21,
    "Soft Error": 23,
    "Hard Error": 18,
}

# Initial application state
DEFAULT_STATE = "Idle"

# Timing settings in seconds
MAIN_LOOP_DELAY = 1
LED_TRANSITION_DELAY = 0.1
STARTUP_MESSAGE_DELAY = 1.5
STARTUP_PROGRESS_DELAY = 1
SHUTDOWN_MESSAGE_DELAY = 2
GOODBYE_MESSAGE_DELAY = 1
DISPLAY_CLEAR_DELAY = 0.2
