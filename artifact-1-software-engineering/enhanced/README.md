## Project Overview

This project uses a client-server model to control a Raspberry Pi LED and LCD state display. The client allows a user to select a machine state and sends the selected state to the Raspberry Pi through serial communication. The server receives the command, validates it, updates the appropriate LED, and displays the current state and time on the LCD.

The server uses a separate clock thread so the time display updates independently while the main thread waits for serial commands. A lock protects all LCD writes so the clock thread and main thread cannot access the display at the same time.

## Supported States

- Running
- Idle
- Soft Error
- Hard Error
- Shutdown

## LCD Layout

- First line: Current date and time

- Second line: Current machine state

## File Descriptions

### config.py
Stores the serial ports, baud rate, LCD dimensions, GPIO pin assignments,timing values, and initial state.

### state_manager.py
Stores the valid system states and manages state validation and transitions.

### serial_manager.py
Opens the serial connection, sends commands, reads commands, and closes the connection.

### hardware_manager.py
Controls the Raspberry Pi LCD and LEDs. It also handles startup messages, state updates, time updates, shutdown messages, and GPIO cleanup.

### display_control_server.py
Runs on the Raspberry Pi and coordinates the serial manager, state manager, and hardware manager.

### display_control_client.py
Displays the user menu, validates menu selections, prevents duplicate state requests, and sends commands to the Raspberry Pi.

### requirements.txt
Lists the Python libraries required to run the project.

## Program Flow

1. The Raspberry Pi server initializes the LCD, LEDs, serial connection, and state manager.

2. The system begins in the Idle state.

3. The Idle LED turns on.

4. The first LCD line displays the current date and time.

5. The second LCD line displays the current state.

6. The server starts a separate clock thread that updates the first LCD line.

7. The main thread waits for commands from the client.

8. The client validates the users' selection and sends the selected state.

9. The server validates the command and updates the current state.

10. The hardware manager changes the active LED and updates the second LCD line.

11. A threading lock prevents simultaneous LCD writes.

12. When Shutdown is received, the server stops and joins the clock thread before displaying shutdown messages and releasing hardware resources.

## Author

Mathew Masar  
Southern New Hampshire University  
CS-499 Computer Science Capstone