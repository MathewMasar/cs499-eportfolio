package AppointmentService;

/*
 * JUnit test class verifies that Appointment correctly stores
 * service-based appointment information and calculates end times.
 *
 * Tests:
 * : valid appointment creation
 * : required-field validation
 * : description and ID boundaries
 * : calculated start and end date/time values
 */

import static org.junit.Assert.*;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;

import org.junit.Test;

public class AppointmentTest {

    // = = Valid Creation Tests = =

    // Verifies that all valid appointment fields are stored correctly.
    @Test
    public void testValidAppointmentCreation() {
        Appointment appointment = new Appointment(
                "ABC123",
                LocalDate.of(2026, 8, 10),
                LocalTime.of(9, 0),
                ServiceType.BASIC_SERVICE,
                "Basic appointment");

        assertEquals("ABC123", appointment.getAppointmentId());
        assertEquals(
                LocalDate.of(2026, 8, 10),
                appointment.getAppointmentDate());
        assertEquals(
                LocalTime.of(9, 0),
                appointment.getStartTime());
        assertEquals(
                ServiceType.BASIC_SERVICE,
                appointment.getServiceType());
        assertEquals(
                "Basic appointment",
                appointment.getDescription());
    }

    // Verifies that a 10-character appointment ID is accepted.
    @Test
    public void testAppointmentIdExactlyTenCharacters() {
        Appointment appointment = new Appointment(
                "1234567890",
                LocalDate.of(2026, 8, 10),
                LocalTime.of(9, 0),
                ServiceType.STANDARD_SERVICE,
                "Maximum ID");

        assertEquals(10, appointment.getAppointmentId().length());
    }

    // = = Time Calculation Tests = =

    // Verifies that start date and time are combined correctly.
    @Test
    public void testGetStartDateTime() {
        Appointment appointment = new Appointment(
                "ABC123",
                LocalDate.of(2026, 8, 10),
                LocalTime.of(9, 30),
                ServiceType.BASIC_SERVICE,
                "Start calculation");

        assertEquals(
                LocalDateTime.of(2026, 8, 10, 9, 30),
                appointment.getStartDateTime());
    }

    // Verifies that a 30-minute service calculates the correct end time.
    @Test
    public void testThirtyMinuteServiceEndTime() {
        Appointment appointment = new Appointment(
                "ABC123",
                LocalDate.of(2026, 8, 10),
                LocalTime.of(9, 0),
                ServiceType.BASIC_SERVICE,
                "Thirty minutes");

        assertEquals(
                LocalDateTime.of(2026, 8, 10, 9, 30),
                appointment.getEndDateTime());
    }

    // Verifies that a 45-minute service calculates the correct end time.
    @Test
    public void testFortyFiveMinuteServiceEndTime() {
        Appointment appointment = new Appointment(
                "ABC123",
                LocalDate.of(2026, 8, 10),
                LocalTime.of(9, 30),
                ServiceType.STANDARD_SERVICE,
                "Forty-five minutes");

        assertEquals(
                LocalDateTime.of(2026, 8, 10, 10, 15),
                appointment.getEndDateTime());
    }

    // Verifies that a 60-minute service calculates the correct end time.
    @Test
    public void testSixtyMinuteServiceEndTime() {
        Appointment appointment = new Appointment(
                "ABC123",
                LocalDate.of(2026, 8, 10),
                LocalTime.of(9, 0),
                ServiceType.PREMIUM_SERVICE,
                "Sixty minutes");

        assertEquals(
                LocalDateTime.of(2026, 8, 10, 10, 0),
                appointment.getEndDateTime());
    }

    // = = Invalid Field Tests = =

    @Test(expected = IllegalArgumentException.class)
    public void testNullAppointmentIdRejected() {
        new Appointment(
                null,
                LocalDate.of(2026, 8, 10),
                LocalTime.of(9, 0),
                ServiceType.BASIC_SERVICE,
                "Invalid ID");
    }

    @Test(expected = IllegalArgumentException.class)
    public void testLongAppointmentIdRejected() {
        new Appointment(
                "ABCDEFGHIJK",
                LocalDate.of(2026, 8, 10),
                LocalTime.of(9, 0),
                ServiceType.BASIC_SERVICE,
                "Invalid ID");
    }

    @Test(expected = IllegalArgumentException.class)
    public void testNullDateRejected() {
        new Appointment(
                "ABC123",
                null,
                LocalTime.of(9, 0),
                ServiceType.BASIC_SERVICE,
                "Invalid date");
    }

    @Test(expected = IllegalArgumentException.class)
    public void testNullStartTimeRejected() {
        new Appointment(
                "ABC123",
                LocalDate.of(2026, 8, 10),
                null,
                ServiceType.BASIC_SERVICE,
                "Invalid time");
    }

    @Test(expected = IllegalArgumentException.class)
    public void testNullServiceTypeRejected() {
        new Appointment(
                "ABC123",
                LocalDate.of(2026, 8, 10),
                LocalTime.of(9, 0),
                null,
                "Invalid service");
    }

    @Test(expected = IllegalArgumentException.class)
    public void testNullDescriptionRejected() {
        new Appointment(
                "ABC123",
                LocalDate.of(2026, 8, 10),
                LocalTime.of(9, 0),
                ServiceType.BASIC_SERVICE,
                null);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testBlankDescriptionRejected() {
        new Appointment(
                "ABC123",
                LocalDate.of(2026, 8, 10),
                LocalTime.of(9, 0),
                ServiceType.BASIC_SERVICE,
                "   ");
    }

    @Test(expected = IllegalArgumentException.class)
    public void testLongDescriptionRejected() {
        new Appointment(
                "ABC123",
                LocalDate.of(2026, 8, 10),
                LocalTime.of(9, 0),
                ServiceType.BASIC_SERVICE,
                "This description is intentionally longer than fifty characters and must fail.");
    }
} // END public class AppointmentTest
