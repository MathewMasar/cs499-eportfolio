package AppointmentService;
/*
 * JUnit test class verifies that Appointment class correctly enforces all field constraints.
 */

import static org.junit.Assert.*;  // JUnit 4
import org.junit.Test;             // JUnit 4 annotation

import java.util.Date;

public class AppointmentTest {

    // = = Valid Creation = =
    @Test
    public void testValidAppointmentCreation() {
        Date future = new Date(System.currentTimeMillis() + 86400000); // +1 day (milliseconds)
        Appointment appt = new Appointment("A1B2C3D4E5", future, "Job interview");
        assertEquals("A1B2C3D4E5", appt.getAppointmentId());
        assertEquals("Job interview", appt.getDescription());
        assertTrue(appt.getAppointmentDate().after(new Date()));
    }

    // = = Invalid ID = =
    @Test
    public void testInvalidAppointmentIdTooLong() {
        Date future = new Date(System.currentTimeMillis() + 1000); // +1 sec buffer (milliseconds)
        try {
            new Appointment("ABCDEFGHIJK", future, "Desc");
            fail("Expected IllegalArgumentException for ID > 10 chars.");
        } catch (IllegalArgumentException e) {
            assertTrue(true);
        }
    }

    @Test
    public void testInvalidAppointmentIdNull() {
        Date future = new Date(System.currentTimeMillis() + 1000); // +1 sec buffer (milliseconds)
        try {
            new Appointment(null, future, "Desc");
            fail("Expected IllegalArgumentException for null ID.");
        } catch (IllegalArgumentException e) {
            assertTrue(true);
        }
    }

    // = = Invalid Date = =
    @Test
    public void testInvalidAppointmentDateNull() {
        try {
            new Appointment("ABC123", null, "Desc");
            fail("Expected IllegalArgumentException for null date.");
        } catch (IllegalArgumentException e) {
            assertTrue(true);
        }
    }

    @Test
    public void testInvalidAppointmentDateInPast() {
        Date past = new Date(System.currentTimeMillis() - 86400000); // -1 day (milliseconds)
        try {
            new Appointment("ABC123", past, "Desc");
            fail("Expected IllegalArgumentException for past date.");
        } catch (IllegalArgumentException e) {
            assertTrue(true);
        }
    }

    // = = Invalid Description = =
    @Test
    public void testInvalidDescriptionTooLong() {
        Date future = new Date(System.currentTimeMillis() + 1000);
        String longDesc = "This description is deffffffffffffffffffffffinitely longer than fifty characters and should fail.";
        try {
            new Appointment("ABC123", future, longDesc);
            fail("Expected IllegalArgumentException for description > 50 chars.");
        } catch (IllegalArgumentException e) {
            assertTrue(true);
        }
    }

    @Test
    public void testInvalidDescriptionNull() {
        Date future = new Date(System.currentTimeMillis() + 1000);
        try {
            new Appointment("ABC123", future, null);
            fail("Expected IllegalArgumentException for null description.");
        } catch (IllegalArgumentException e) {
            assertTrue(true);
        }
    }
} // END public class AppointmentTest