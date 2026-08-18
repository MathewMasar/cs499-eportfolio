#
# hardware_manager.py - This file runs on the Raspberry Pi and is the
# only component that directly controls the LCD display and status LEDs.
# It initializes hardware, applies state changes, updates the clock, and
# releases all GPIO and display resources during shutdown.
#
#------------------------------------------------------------------
# Change History
#------------------------------------------------------------------
# Version   |   Description
#------------------------------------------------------------------
#    1          Initial Enhanced Development
#------------------------------------------------------------------

import threading
from datetime import datetime
from time import sleep
from typing import Dict, List

import adafruit_character_lcd.character_lcd as characterlcd
import board
import digitalio
import RPi.GPIO as GPIO

from config import (
    DISPLAY_CLEAR_DELAY,
    GOODBYE_MESSAGE_DELAY,
    LCD_COLUMNS,
    LCD_ROWS,
    LED_PINS,
    LED_TRANSITION_DELAY,
    SHUTDOWN_MESSAGE_DELAY,
    STARTUP_MESSAGE_DELAY,
    STARTUP_PROGRESS_DELAY,
)


class HardwareManager:
    # Owns all LCD and LED setup, updates, and cleanup operations.

    def __init__(self) -> None:
        self._lcd = None
        self._lcd_pins: List[digitalio.DigitalInOut] = []
        self._led_pins: Dict[str, int] = dict(LED_PINS)
        self._initialized = False
        self._lcd_lock = threading.Lock()

    def initialize(self) -> None:
        # Configures the LCD interface and all state LEDs.
        if self._initialized:
            return

        lcd_rs = digitalio.DigitalInOut(board.D17)
        lcd_en = digitalio.DigitalInOut(board.D27)
        lcd_d4 = digitalio.DigitalInOut(board.D5)
        lcd_d5 = digitalio.DigitalInOut(board.D6)
        lcd_d6 = digitalio.DigitalInOut(board.D13)
        lcd_d7 = digitalio.DigitalInOut(board.D26)

        self._lcd_pins = [
            lcd_rs,
            lcd_en,
            lcd_d4,
            lcd_d5,
            lcd_d6,
            lcd_d7,
        ]

        self._lcd = characterlcd.Character_LCD_Mono(
            lcd_rs,
            lcd_en,
            lcd_d4,
            lcd_d5,
            lcd_d6,
            lcd_d7,
            LCD_COLUMNS,
            LCD_ROWS,
        )

        with self._lcd_lock:
            self._lcd.clear()

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        for pin in self._led_pins.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

        self._initialized = True

    def display_startup(self) -> None:
        # Displays the original welcome and initialization sequence.
        self._require_initialized()

        with self._lcd_lock:
            self._lcd.clear()
            self._lcd.message = "Welcome\nInitializing..."

        sleep(STARTUP_MESSAGE_DELAY)

        with self._lcd_lock:
            self._lcd.clear()
            self._lcd.message = "      ...      "

        sleep(STARTUP_PROGRESS_DELAY)

        with self._lcd_lock:
            self._lcd.clear()

    def apply_state(self, state: str) -> None:
        # Turns off the previous LEDs, turns on the LED associated with the
        # supplied state, and updates line two of the LCD.
        self._require_initialized()

        if state not in self._led_pins:
            raise ValueError(f"No LED is configured for state: {state}")

        self._turn_off_all_leds()
        sleep(LED_TRANSITION_DELAY)
        GPIO.output(self._led_pins[state], True)

        with self._lcd_lock:
            self._lcd.cursor_position(0, 1)
            self._lcd.message = " " * LCD_COLUMNS
            self._lcd.cursor_position(0, 1)
            self._lcd.message = state[:LCD_COLUMNS]

    def update_time(self) -> None:
        # Updates line one of the LCD with the current date and time.
        self._require_initialized()

        current_time = datetime.now().strftime(
            "%b %d %H:%M:%S"
        )[:LCD_COLUMNS]

        with self._lcd_lock:
            self._lcd.cursor_position(0, 0)
            self._lcd.message = " " * LCD_COLUMNS
            self._lcd.cursor_position(0, 0)
            self._lcd.message = current_time

    def display_shutdown(self) -> None:
        # Displays the original shutdown and goodbye messages.
        if not self._initialized or self._lcd is None:
            return

        with self._lcd_lock:
            self._lcd.clear()
            self._lcd.message = "Shutting down..."

        sleep(SHUTDOWN_MESSAGE_DELAY)

        with self._lcd_lock:
            self._lcd.clear()

        sleep(DISPLAY_CLEAR_DELAY)

        with self._lcd_lock:
            self._lcd.message = "    Goodbye    "

        sleep(GOODBYE_MESSAGE_DELAY)

    def cleanup(self) -> None:
        # Turns off LEDs and releases all LCD and GPIO resources.
        if not self._initialized:
            return

        try:
            self._turn_off_all_leds()
        finally:
            GPIO.cleanup()

        if self._lcd is not None:
            with self._lcd_lock:
                self._lcd.clear()
            sleep(DISPLAY_CLEAR_DELAY)

        for pin in self._lcd_pins:
            try:
                pin.deinit()
            except Exception:
                # Continue cleanup even if one display pin was already released.
                pass

        self._initialized = False

    def _turn_off_all_leds(self) -> None:
        # Turns off every configured state LED.
        for pin in self._led_pins.values():
            GPIO.output(pin, False)

    def _require_initialized(self) -> None:
        # Prevents hardware operations before initialization.
        if not self._initialized or self._lcd is None:
            raise RuntimeError("HardwareManager has not been initialized.")
