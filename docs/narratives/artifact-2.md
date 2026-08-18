# Enhancement Narrative

## Artifact Description

The Appointment Service was originally created in CS 320: Software Testing, Automation, and Quality Assurance. The original project consisted of an `Appointment` class and an `AppointmentService` class supported by JUnit tests for object creation, validation, and appointment management. Its primary purpose was to demonstrate object-oriented programming and automated testing rather than function as a complete scheduling application.

For my capstone, I expanded the artifact into a more realistic appointment scheduling system for a consulting firm. The enhanced application supports three consultation service tiers: **Basic, Standard, and Premium**, with appointment durations of 30, 45, and 60 minutes. Each service maintains an independent schedule while enforcing business hours, preventing scheduling conflicts, generating valid appointment slots, and supporting simultaneous appointments across different service tiers.

## Enhancement and Skills Demonstrated

The primary goal of this enhancement was to demonstrate the selection and application of appropriate algorithms and data structures. Instead of relying on one collection for every operation, the enhanced application combines several structures based on their specific strengths:

- **HashMap** provides direct appointment lookup by identifier.
- **EnumMap** organizes independent schedules by consultation service.
- **TreeMap** maintains appointments in chronological order.
- **PriorityQueue** provides efficient access to the next upcoming appointment.

This design demonstrates that selecting a data structure depends on the operations a system needs to perform. Rather than replacing the original `HashMap`, I preserved it for the operation it handles well and introduced complementary structures for chronological and service-specific scheduling.

The scheduling logic was also expanded substantially. Appointments must begin no earlier than **8:00 AM** and finish by **8:00 PM**, with available slots generated according to the duration of the selected service. Conflicting appointments within the same service are prevented automatically, while different service tiers can operate simultaneously because they maintain independent schedules.

Software reliability was strengthened through an expanded suite of **37 JUnit tests** covering appointment validation, service durations, slot generation, business-hour boundaries, scheduling conflicts, deletion, chronological retrieval, and next-appointment retrieval. A fixed system clock was also introduced so time-dependent tests remain deterministic and repeatable.

Finally, I added a console demonstration that shows the scheduling engine creating appointments, retrieving upcoming appointments, and displaying schedules chronologically. This provides a practical demonstration of the underlying data structures working together beyond the automated test suite.

## Course Outcomes

This enhancement demonstrates my ability to design and evaluate computing solutions using appropriate algorithms and data structures. Each structure was selected according to the operations it supports, while considering efficiency, maintainability, and scalability.

It also demonstrates software engineering practices through object-oriented design, validation, automated testing, deterministic time-based testing, and the extension of existing functionality without unnecessarily replacing working code.

The project further supports reliability and secure development practices through validation of scheduling requests and enforcement of business rules before application data is modified. Clear organization, documentation, and separation of responsibilities also make the reasoning behind the scheduling design easier for another developer to understand and maintain.

## Reflection

One of the most important lessons from this enhancement was that no single data structure is necessarily appropriate for every operation. The original application could successfully store appointments in one collection, but the expanded scheduling requirements made the limitations of that approach much clearer.

Combining multiple structures allowed each one to solve a specific problem while keeping the overall scheduling logic organized. Although the performance difference is relatively small for an application of this size, these design decisions become increasingly important as a system grows. A production scheduling platform handling thousands of appointments could otherwise spend unnecessary time repeatedly searching, sorting, and reorganizing the same information.

The enhancement also gave me a greater appreciation for designing software around business requirements. Appointment duration, operating hours, service types, availability, and conflict detection all directly influenced the application's algorithms and architecture. Adding even a small number of realistic requirements demonstrated how quickly scheduling systems can become complex.

Expanding the project to 37 automated tests reinforced another important lesson: as software functionality grows, the number of scenarios requiring verification grows with it. Reliable applications need repeatable testing and strong validation so that changes in one area do not unexpectedly affect another.

Overall, this enhancement transformed a relatively simple appointment-management assignment into a more complete scheduling system. It demonstrates how thoughtful data-structure selection, algorithm design, validation, and automated testing can improve the scalability, maintainability, and reliability of an existing application.