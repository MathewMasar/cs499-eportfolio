package AppointmentService;
/*
 * JUnit test class verifies that AppointmentService class correctly manages appointments.
 * It tests:
 * : Adding a new appointment with unique appointmentId
 * : Deleting an appointment by appointmentId (valid and not)
 */

import static org.junit.Assert.*;  // JUnit 4
import org.junit.Test;             // JUnit 4 annotation

import java.util.Date;

public class AppointmentServiceTest {

    // = = Add Appointment Tests = =
    @Test
    public void testAddAppointmentValid() {
        AppointmentService service = new AppointmentService();
        Date future = new Date(System.currentTimeMillis() + 60_000); // +1 minute buffer (milliseconds)

        service.addAppointment(future, "Oil change");

        Appointment added = service.getAllAppointments().values().iterator().next();
        assertNotNull(added);
        assertEquals("Oil change", added.getDescription());
        assertTrue(added.getAppointmentDate().after(new Date()));
        assertNotNull(added.getAppointmentId());
        assertTrue(added.getAppointmentId().length() <= 10);
    }

    // = = Delete Appointment Tests = =
    @Test
    public void testDeleteAppointmentValid() {
        AppointmentService service = new AppointmentService();
        Date future = new Date(System.currentTimeMillis() + 60_000);

        service.addAppointment(future, "Follow-up visit");
        String id = service.getAllAppointments().keySet().iterator().next();

        service.deleteAppointment(id);

        assertFalse(service.getAllAppointments().containsKey(id));
    }

    @Test
    public void testDeleteAppointmentNonExistent() {
        AppointmentService service = new AppointmentService();
        try {
            service.deleteAppointment("ZZZZZZZZZZ"); // not valid ID
            fail("Expected IllegalArgumentException for non-existent appointment ID.");
        } catch (IllegalArgumentException e) {
            assertTrue(true);
        }
    }
} // END public class AppointmentServiceTest