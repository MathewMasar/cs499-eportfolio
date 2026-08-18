# Appointment Service Scheduler

This enhanced CS-499 artifact redesigns the original appointment service into a tiered scheduling system for a consulting firm. Clients may schedule Basic, Standard, or Premium consultations, with each service maintaining its own appointment schedule and business rules to support efficient scheduling and conflict prevention.

## Services

- Basic Consultation (30 Minutes)
- Standard Consultation (45 Minutes)
- Premium Consultation (60 Minutes)


## Scheduling Rules

- Appointments begin no earlier than 8:00 AM.
- Appointments must end by 8:00 PM.
- Each service generates slots according to its own duration.
- Two appointments in the same service cannot occupy the same slot.
- Different services may be booked at the same time because each has an independent schedule.
- Past dates and past time slots are rejected.

## Data Structures

- `HashMap<String, Appointment>` supports lookup and deletion by ID.
- `EnumMap<ServiceType, TreeMap<LocalDateTime, Appointment>>` stores one chronological schedule for each service.
- `PriorityQueue<Appointment>` provides the next upcoming appointment across all services.
- Each service-specific `TreeMap` also supports retrieving the next appointment for that individual service.

## Project Structure

```text
src/main/java/AppointmentService/
    Appointment.java
    AppointmentService.java
    SchedulerDemo.java
    ServiceType.java

src/test/java/AppointmentService/
    AppointmentTest.java
    AppointmentServiceTest.java
```

## Automated Testing

The project includes **37 JUnit 4 tests** that verify the appointment model and scheduling service.

### Appointment Tests

The `AppointmentTest` suite verifies:

- Valid appointment creation and field storage
- Appointment ID length constraints
- Required date, time, service, and description fields
- Description length and blank-value validation
- Start date/time calculation
- End-time calculation for Basic, Standard, and Premium consultations

### Appointment Service Tests

The `AppointmentServiceTest` suite verifies:

- Correct duration configuration for all three services
- Daily slot generation for each service tier
- Valid appointment scheduling
- Removal of booked slots from availability
- Duplicate-booking prevention within the same service
- Simultaneous bookings across independent service schedules
- Rejection of invalid service-specific start times
- Opening and closing time boundaries
- Appointment deletion and restored slot availability
- Chronological retrieval across all services
- Next appointment retrieval across all services
- Next appointment retrieval for each individual service
- Service-specific and date-specific appointment retrieval
- Rejection of past dates, null services, and invalid configuration

## Requirements

- Java 21 or later
- Apache Maven

## Run Tests

```bash
mvn clean test
```

A successful run should display:

```text
Tests run: 37, Failures: 0, Errors: 0, Skipped: 0

BUILD SUCCESS
```

## Run Demo

The project includes a console demonstration that showcases the scheduling engine by creating sample appointments and displaying the scheduler's functionality.

### Visual Studio Code (Recommended)

Open `SchedulerDemo.java` and click **Run** above the `main()` method.

### Maven

If the `exec-maven-plugin` is configured in `pom.xml`, navigate to the project directory containing `pom.xml` and run:

```bash
mvn exec:java
```

Alternatively, you can specify the main class explicitly:

```bash
mvn exec:java "-Dexec.mainClass=AppointmentService.SchedulerDemo"
```

> **Note:** Run all Maven commands from the project directory that contains `pom.xml`.

The demonstration showcases:

- Scheduling appointments for Basic, Standard, and Premium consultations
- Service-specific appointment slot generation
- Next appointment retrieval for each service tier
- Chronological display of all scheduled appointments
- Independent scheduling across service tiers