package AppointmentService;

/*
 * JUnit test class verifies that AppointmentService correctly manages
 * three independent service schedules.
 *
 * Tests:
 * : service duration and slot generation
 * : independent chair availability
 * : appointment creation and validation
 * : business-hour boundaries
 * : deletion and restored availability
 * : chronological and next-appointment retrieval
 * : fixed-clock handling for predictable time-based tests
 */

import static org.junit.Assert.*;

import java.time.Clock;
import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.ZoneId;
import java.util.List;

import org.junit.Before;
import org.junit.Test;

public class AppointmentServiceTest {

    // = = Fixed Test Time = =
    private static final ZoneId TEST_ZONE =
            ZoneId.of("America/New_York");

    private static final Clock FIXED_CLOCK =
            Clock.fixed(
                    Instant.parse("2026-08-04T13:00:00Z"),
                    TEST_ZONE);

    private AppointmentService service;
    private LocalDate futureDate;

    @Before
    public void setUp() {
        service = new AppointmentService(FIXED_CLOCK);
        futureDate = LocalDate.of(2026, 8, 10);
    }

    // = = Service Type Tests = =

    // Verifies the duration assigned to each service.
    @Test
    public void testServiceDurations() {
        assertEquals(
                30,
                ServiceType.BASIC_SERVICE.getDurationMinutes());
        assertEquals(
                45,
                ServiceType.STANDARD_SERVICE.getDurationMinutes());
        assertEquals(
                60,
                ServiceType.PREMIUM_SERVICE.getDurationMinutes());
    }

    // = = Slot Generation Tests = =

    // Verifies that the 30-minute service provides 24 daily slots.
    @Test
    public void testThirtyMinuteServiceSlotGeneration() {
        List<LocalTime> slots = service.getAvailableSlots(
                futureDate,
                ServiceType.BASIC_SERVICE);

        assertEquals(24, slots.size());
        assertEquals(LocalTime.of(8, 0), slots.get(0));
        assertEquals(LocalTime.of(19, 30), slots.get(23));
    }

    // Verifies that the 45-minute service provides 16 daily slots.
    @Test
    public void testFortyFiveMinuteServiceSlotGeneration() {
        List<LocalTime> slots = service.getAvailableSlots(
                futureDate,
                ServiceType.STANDARD_SERVICE);

        assertEquals(16, slots.size());
        assertEquals(LocalTime.of(8, 0), slots.get(0));
        assertEquals(LocalTime.of(19, 15), slots.get(15));
    }

    // Verifies that the 60-minute service provides 12 daily slots.
    @Test
    public void testSixtyMinuteServiceSlotGeneration() {
        List<LocalTime> slots = service.getAvailableSlots(
                futureDate,
                ServiceType.PREMIUM_SERVICE);

        assertEquals(12, slots.size());
        assertEquals(LocalTime.of(8, 0), slots.get(0));
        assertEquals(LocalTime.of(19, 0), slots.get(11));
    }

    // = = Scheduling Tests = =

    // Verifies that a valid selected slot creates an appointment.
    @Test
    public void testScheduleValidAppointment() {
        Appointment appointment = service.scheduleAppointment(
                futureDate,
                LocalTime.of(8, 0),
                ServiceType.BASIC_SERVICE,
                "Valid booking");

        assertNotNull(appointment);
        assertEquals(
                ServiceType.BASIC_SERVICE,
                appointment.getServiceType());
        assertEquals(
                LocalTime.of(8, 0),
                appointment.getStartTime());
        assertEquals(
                "Valid booking",
                appointment.getDescription());
    }

    // Verifies that scheduling removes the chosen slot from availability.
    @Test
    public void testScheduledSlotRemovedFromAvailability() {
        service.scheduleAppointment(
                futureDate,
                LocalTime.of(8, 0),
                ServiceType.BASIC_SERVICE,
                "Reserved");

        List<LocalTime> slots = service.getAvailableSlots(
                futureDate,
                ServiceType.BASIC_SERVICE);

        assertFalse(slots.contains(LocalTime.of(8, 0)));
        assertEquals(23, slots.size());
    }

    // Verifies that the same service cannot book the same chair twice.
    @Test(expected = IllegalArgumentException.class)
    public void testDuplicateSlotWithinSameServiceRejected() {
        service.scheduleAppointment(
                futureDate,
                LocalTime.of(8, 0),
                ServiceType.BASIC_SERVICE,
                "First booking");

        service.scheduleAppointment(
                futureDate,
                LocalTime.of(8, 0),
                ServiceType.BASIC_SERVICE,
                "Duplicate booking");
    }

    // Verifies that different services may use their independent chairs
    // at the same date and time without creating a conflict.
    @Test
    public void testDifferentServicesCanBookSameTime() {
        Appointment shortAppointment =
                service.scheduleAppointment(
                        futureDate,
                        LocalTime.of(8, 0),
                        ServiceType.BASIC_SERVICE,
                        "Short service");

        Appointment extendedAppointment =
                service.scheduleAppointment(
                        futureDate,
                        LocalTime.of(8, 0),
                        ServiceType.PREMIUM_SERVICE,
                        "Premium service");

        assertNotNull(shortAppointment);
        assertNotNull(extendedAppointment);
        assertEquals(2, service.getAllAppointments().size());
    }

    // Verifies that a time not aligned with the selected service's
    // required interval is rejected.
    @Test(expected = IllegalArgumentException.class)
    public void testInvalidServiceSlotRejected() {
        service.scheduleAppointment(
                futureDate,
                LocalTime.of(8, 30),
                ServiceType.STANDARD_SERVICE,
                "Invalid 45-minute slot");
    }

    // = = Business Hour Tests = =

    // Verifies that an appointment beginning before 8:00 AM is rejected.
    @Test(expected = IllegalArgumentException.class)
    public void testAppointmentBeforeOpeningRejected() {
        service.scheduleAppointment(
                futureDate,
                LocalTime.of(7, 30),
                ServiceType.BASIC_SERVICE,
                "Before opening");
    }

    // Verifies that an appointment ending exactly at 8:00 PM is accepted.
    @Test
    public void testAppointmentEndingAtClosingAccepted() {
        Appointment appointment = service.scheduleAppointment(
                futureDate,
                LocalTime.of(19, 30),
                ServiceType.BASIC_SERVICE,
                "Closing appointment");

        assertEquals(
                LocalTime.of(20, 0),
                appointment.getEndDateTime().toLocalTime());
    }

    // Verifies that a start time causing the appointment to end after
    // 8:00 PM is rejected.
    @Test(expected = IllegalArgumentException.class)
    public void testAppointmentEndingAfterClosingRejected() {
        service.scheduleAppointment(
                futureDate,
                LocalTime.of(19, 45),
                ServiceType.BASIC_SERVICE,
                "After closing");
    }

    // = = Deletion and Availability Tests = =

    // Verifies that deleting an appointment restores its service slot.
    @Test
    public void testDeleteAppointmentRestoresAvailability() {
        Appointment appointment = service.scheduleAppointment(
                futureDate,
                LocalTime.of(8, 0),
                ServiceType.STANDARD_SERVICE,
                "Delete and restore");

        assertFalse(
                service.getAvailableSlots(
                        futureDate,
                        ServiceType.STANDARD_SERVICE)
                        .contains(LocalTime.of(8, 0)));

        service.deleteAppointment(
                appointment.getAppointmentId());

        assertTrue(
                service.getAvailableSlots(
                        futureDate,
                        ServiceType.STANDARD_SERVICE)
                        .contains(LocalTime.of(8, 0)));
    }

    // Verifies that deleting an unknown ID is rejected.
    @Test(expected = IllegalArgumentException.class)
    public void testDeleteUnknownAppointmentRejected() {
        service.deleteAppointment("UNKNOWN123");
    }

    // = = Retrieval Tests = =

    // Verifies that appointments are returned in chronological order
    // even when entered in a different order.
    @Test
    public void testAppointmentsReturnedChronologically() {
        service.scheduleAppointment(
                futureDate,
                LocalTime.of(10, 0),
                ServiceType.PREMIUM_SERVICE,
                "Third");

        service.scheduleAppointment(
                futureDate,
                LocalTime.of(8, 0),
                ServiceType.BASIC_SERVICE,
                "First");

        service.scheduleAppointment(
                futureDate,
                LocalTime.of(8, 45),
                ServiceType.STANDARD_SERVICE,
                "Second");

        List<Appointment> appointments =
                service.getAppointmentsChronologically(); // Returns all appointments in chronological order    

        assertEquals("First", appointments.get(0).getDescription());
        assertEquals("Second", appointments.get(1).getDescription());
        assertEquals("Third", appointments.get(2).getDescription());
    }

    // Verifies that the overall priority queue returns the earliest
    // upcoming appointment across all three services.
    @Test
    public void testGetNextAppointmentAcrossServices() {
        service.scheduleAppointment(
                futureDate,
                LocalTime.of(9, 0),
                ServiceType.PREMIUM_SERVICE,
                "Later");

        service.scheduleAppointment(
                futureDate,
                LocalTime.of(8, 0),
                ServiceType.BASIC_SERVICE,
                "Earliest");

        assertEquals(
                "Earliest",
                service.getNextAppointment().getDescription());
    }

    // Verifies that each service returns its own next upcoming appointment
    // without being affected by earlier appointments in another service.
    @Test
    public void testGetNextAppointmentForEachService() {
        service.scheduleAppointment(
                futureDate,
                LocalTime.of(9, 0),
                ServiceType.BASIC_SERVICE,
                "Next basic service");

        service.scheduleAppointment(
                futureDate,
                LocalTime.of(8, 45),
                ServiceType.STANDARD_SERVICE,
                "Next standard service");

        service.scheduleAppointment(
                futureDate,
                LocalTime.of(8, 0),
                ServiceType.PREMIUM_SERVICE,
                "Next premium service");

        assertEquals(
                "Next basic service",
                service.getNextAppointmentForService(
                        ServiceType.BASIC_SERVICE)
                        .getDescription());

        assertEquals(
                "Next standard service",
                service.getNextAppointmentForService(
                        ServiceType.STANDARD_SERVICE)
                        .getDescription());

        assertEquals(
                "Next premium service",
                service.getNextAppointmentForService(
                        ServiceType.PREMIUM_SERVICE)
                        .getDescription());
    }

    // Verifies that service-specific next retrieval returns null when
    // the selected service has no upcoming appointments.
    @Test
    public void testGetNextAppointmentForServiceReturnsNullWhenEmpty() {
        assertNull(
                service.getNextAppointmentForService(
                        ServiceType.BASIC_SERVICE));
    }

    // Verifies that service-specific retrieval returns only appointments
    // belonging to the selected service schedule.
    @Test
    public void testGetAppointmentsForService() {
        service.scheduleAppointment(
                futureDate,
                LocalTime.of(8, 0),
                ServiceType.BASIC_SERVICE,
                "Short");

        service.scheduleAppointment(
                futureDate,
                LocalTime.of(8, 0),
                ServiceType.PREMIUM_SERVICE,
                "Extended");

        List<Appointment> shortAppointments =
                service.getAppointmentsForService(
                        ServiceType.BASIC_SERVICE);

        assertEquals(1, shortAppointments.size());
        assertEquals(
                ServiceType.BASIC_SERVICE,
                shortAppointments.get(0).getServiceType());
    }

    // Verifies that date retrieval combines all service chairs for
    // the selected day without including another date.
    @Test
    public void testGetAppointmentsForDate() {
        service.scheduleAppointment(
                futureDate,
                LocalTime.of(8, 0),
                ServiceType.BASIC_SERVICE,
                "Selected date");

        service.scheduleAppointment(
                futureDate.plusDays(1),
                LocalTime.of(8, 0),
                ServiceType.BASIC_SERVICE,
                "Other date");

        List<Appointment> appointments =
                service.getAppointmentsForDate(futureDate);

        assertEquals(1, appointments.size());
        assertEquals(
                "Selected date",
                appointments.get(0).getDescription());
    }

    // = = Validation Tests = =

    @Test(expected = IllegalArgumentException.class)
    public void testPastDateRejected() {
        service.getAvailableSlots(
                LocalDate.of(2026, 8, 3),
                ServiceType.BASIC_SERVICE);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testNullServiceRejected() {
        service.getAvailableSlots(futureDate, null);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testNullClockRejected() {
        new AppointmentService(null);
    }
} // END public class AppointmentServiceTest
