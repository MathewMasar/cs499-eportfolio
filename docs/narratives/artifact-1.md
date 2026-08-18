# Enhancement Narrative

## Artifact Description

The LED/LCD State Simulator was originally created in CS 350: Emerging Systems Architectures and Technologies. It is a client-server state machine application that uses serial communication to connect a client application with a Raspberry Pi controlling a 16x2 LCD display and four LEDs. User-selected machine states are transmitted to the Raspberry Pi, which updates the display and LEDs to represent the current system status.

For my capstone, I enhanced the artifact primarily through software engineering and design. Rather than changing its purpose, I reorganized the application to improve its architecture, maintainability, reliability, and extensibility while preserving the original client-server and hardware functionality.

## Enhancement and Skills Demonstrated

The most significant improvement was separating responsibilities that were previously handled within larger scripts. I introduced three primary components:

- **HardwareManager** encapsulates LCD and GPIO operations.
- **SerialManager** isolates serial communication.
- **StateManager** centralizes machine-state validation and transitions.

This reduced coupling and gave each part of the application a clearly defined responsibility. The resulting architecture better demonstrates object-oriented design, modularity, separation of concerns, and the ability to evaluate and improve an existing software system.

I also introduced a centralized `config.py` module for GPIO assignments, serial settings, display configuration, and shared constants. Hardware or communication settings can now be changed in one location rather than being scattered throughout the application. This makes the project easier to configure, maintain, and adapt to different hardware environments.

Reliability was strengthened through improved input validation, structured logging, exception handling, centralized hardware control, and more dependable resource cleanup during shutdown.

One enhancement that extended beyond my original plan was multithreading. The original server updated the LCD clock within the same loop responsible for processing serial commands. I moved the clock to an independent thread so display updates no longer depend on command processing. Because both execution paths can access the LCD, I also implemented synchronization using a lock to prevent concurrent writes to the shared hardware resource.

## Course Outcomes

This enhancement demonstrates my ability to evaluate an existing computing solution and improve it using professional software engineering practices. The redesigned architecture demonstrates modular design, object-oriented programming, concurrent processing, synchronization, configuration management, validation, and defensive programming.

The enhancement also supports collaboration and communication through clearer project organization, comments, documentation, and well-defined component responsibilities. Another developer can more easily understand where hardware control, communication, configuration, and state management occur without tracing the entire application.

Reliability and security considerations are demonstrated through stronger validation, controlled access to shared resources, exception handling, and predictable cleanup of hardware and serial resources.

## Reflection

The most important lesson from this enhancement was that working software is not necessarily well-designed software. The original project successfully met its functional requirements, but revisiting it showed how quickly maintainability becomes difficult when many responsibilities are tightly coupled.

Breaking the application into smaller components made the system easier to understand and reduced duplicated or scattered logic. The multithreading enhancement also gave me practical experience managing shared resources. Adding a synchronization lock reinforced why concurrent execution requires careful consideration when multiple parts of a program interact with the same hardware.

Most importantly, this enhancement changed how I think about writing software for other developers. Returning to my own code months later showed me how valuable clear organization and documentation can be. A maintainable application should communicate its structure and intent to the next developer, not only function correctly for its original author.

Overall, the enhancement preserved the functionality that made the original artifact meaningful while transforming its internal design into a more modular, reliable, configurable, and maintainable embedded application.