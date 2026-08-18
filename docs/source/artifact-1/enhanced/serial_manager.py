#
# serial_manager.py - This file manages serial communication for both
# the client and Raspberry Pi server. It opens, reads from, writes to,
# and safely closes a serial connection while handling invalid byte data.
#
#------------------------------------------------------------------
# Change History
#------------------------------------------------------------------
# Version   |   Description
#------------------------------------------------------------------
#    1          Initial Enhanced Development
#------------------------------------------------------------------

from typing import Optional

import serial


class SerialManager:
    # Wraps a PySerial connection and provides safe text communication.

    def __init__(self, port: str, baud_rate: int, timeout: float) -> None:
        self._serial = serial.Serial(
            port=port,
            baudrate=baud_rate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=timeout,
        )

    def read_command(self) -> Optional[str]:
        # Reads one newline-terminated command.
        #
        # Returns None when no data is available when the command is empty,
        # or when the data cannot be decoded.
        raw_data = self._serial.readline()

        if not raw_data:
            return None

        try:
            command = raw_data.decode("utf-8").strip()
        except UnicodeDecodeError:
            return None

        return command if command else None

    def send_command(self, command: str) -> None:
        # Sends a nonempty newline-terminated command.
        if not isinstance(command, str) or not command.strip():
            raise ValueError("Command cannot be empty.")

        self._serial.write(f"{command.strip()}\n".encode("utf-8"))

    def close(self) -> None:
        # Closes the serial connection when it is open.
        if self._serial.is_open:
            self._serial.close()
