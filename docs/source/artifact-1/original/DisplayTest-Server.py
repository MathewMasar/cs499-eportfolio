#
# DisplayControl-Server.py - This code runs on the Raspberry Pi and is responsible
# for controlling the LCD display and managing the current system state.
# It listens for incoming serial commands from the client and updates the
# display accordingly.
#
#------------------------------------------------------------------
# Change History
#------------------------------------------------------------------
# Version   |   Description
#------------------------------------------------------------------
#    1          Initial Development
#------------------------------------------------------------------

from datetime import datetime
from time import sleep

# serial communication module
import serial

# GPIO / LCD libraries
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

import RPi.GPIO as GPIO


# setupLCD - Method used to configure the LCD display interface
def setupLCD():

    # Modify this if you have a different sized character LCD
    lcd_columns = 16
    lcd_rows = 2

    # Setup GPIO lines to communicate with display
    lcd_rs = digitalio.DigitalInOut(board.D17)
    lcd_en = digitalio.DigitalInOut(board.D27)
    lcd_d4 = digitalio.DigitalInOut(board.D5)
    lcd_d5 = digitalio.DigitalInOut(board.D6)
    lcd_d6 = digitalio.DigitalInOut(board.D13)
    lcd_d7 = digitalio.DigitalInOut(board.D26)

    # Initialize LCD object
    lcd = characterlcd.Character_LCD_Mono(
        lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
        lcd_columns, lcd_rows
    )

    # Clear display before use
    lcd.clear()

    return lcd, lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7



# Method used to cleanup digitalIO 
def cleanupDisplay(lcd, a, b, c, d, e, f):
    lcd.clear()
    sleep(0.5)

    # Deinitialize GPIO lines
    a.deinit()
    b.deinit()
    c.deinit()
    d.deinit()
    e.deinit()
    f.deinit()

def setupLEDs():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # Define GPIO pins for each state
    running_LED = 25
    idle_LED = 21
    soft_LED = 23
    hard_LED = 18

    # Setup only the running LED for now
    GPIO.setup(running_LED, GPIO.OUT)
    GPIO.output(running_LED, False)

    GPIO.setup(idle_LED, GPIO.OUT)
    GPIO.setup(soft_LED, GPIO.OUT)
    GPIO.setup(hard_LED, GPIO.OUT)

    GPIO.output(idle_LED, False)
    GPIO.output(soft_LED, False)
    GPIO.output(hard_LED, False)

    return running_LED, idle_LED, soft_LED, hard_LED


def cleanupLEDs(running_LED, idle_LED, soft_LED, hard_LED):
    # Turn everything off first
    GPIO.output(running_LED, False)
    GPIO.output(idle_LED, False)
    GPIO.output(soft_LED, False)
    GPIO.output(hard_LED, False)

    # Then release GPIO
    GPIO.cleanup()

# Handles shutdown of display and GPIO
def shutdownSystem(lcd, lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7):
    lcd.clear()
    lcd.message = "Shutting down..."
    sleep(2)

    lcd.clear()
    sleep(0.2)
    lcd.message = "    Goodbye    "
    sleep(1)

    cleanupDisplay(lcd, lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7)


# Displays startup message and initializes state
def startupSystem(lcd):
    currentState = "Idle"

    lcd.clear()
    lcd.message = "Welcome\nInitializing..."
    sleep(1.5)
    lcd.clear()
    lcd.message = "      ...      "
    sleep(1)
    lcd.clear()
    return currentState


# Updates LCD with current state and time
def updateStateLine(lcd, currentState):
    lcd.cursor_position(0, 0)
    lcd.message = " " * 16
    lcd.cursor_position(0, 0)
    lcd.message = currentState

# Updates time line of LCD
def updateTime(lcd):
    lcd.cursor_position(0, 1)
    lcd.message = datetime.now().strftime("%b %d %H:%M:%S")

# turn off previous LED
def StatusLedOff(pin):
    GPIO.output(pin, False)
    sleep(0.1)

# turn on new LED
def StatusLedOn(pin):
    GPIO.output(pin, True)
        

# Configure serial connection on Raspberry Pi UART
ser = serial.Serial(
    port="/dev/ttyS0",          # Pi UART interface
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.1
)


# Setup LCD
lcd, lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7 = setupLCD()

# Setup LEDs
running_LED, idle_LED, soft_LED, hard_LED = setupLEDs()

# used for eextra validation even though serial data from client should be sanitized already
VALID_STATES = {
    "Running": running_LED,
    "Idle": idle_LED,          
    "Soft Error": soft_LED,
    "Hard Error": hard_LED
}


### MAIN METHOD ###   

# Initialize system state
currentState = startupSystem(lcd)

StatusLedOn(VALID_STATES[currentState])  # Turn on LED for initial state
updateStateLine(lcd, currentState)  # Update state line on display
updateTime(lcd)  # Update time line on display






repeat = True

try:
    # continuously updates display and checks for commands
    while repeat:

        # Read incoming serial command
        command = ser.readline().decode("utf-8").strip().title()

        # Process command if received
        if command:
            prevState = currentState
            
            # Turn off LED for previous state
            StatusLedOff(VALID_STATES[prevState])
            
            if command == "Shutdown":
                repeat = False
                
            elif command in VALID_STATES:
                currentState = command
                
                # Turn on LED for new state
                StatusLedOn(VALID_STATES[currentState])
                
                updateStateLine(lcd, currentState)

        updateTime(lcd)
        
        # control update rate
        sleep(1)

except KeyboardInterrupt:
    repeat = False

# Perform cleanup on exit
shutdownSystem(lcd, lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7)
cleanupLEDs(running_LED, idle_LED, soft_LED, hard_LED)