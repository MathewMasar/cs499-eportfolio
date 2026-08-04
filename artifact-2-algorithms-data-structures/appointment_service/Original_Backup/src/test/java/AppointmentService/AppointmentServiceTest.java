package AppointmentService;

/*
 * JUnit test class verifies that AppointmentService class correctly manages
 * appointments.
 *
 * Tests:
 * : Adding appointments
 * : Deleting appointments
 * : Retrieving the next upcoming appointment
 * : Retrieving appointments in chronological order
 * : Retrieving appointments within a date range
 */

import static org.junit.Assert.*;

import java.util.Calendar;
import java.util.Date;
import java.util.List;

import org.junit.Test;

public class AppointmentServiceTest {

    // = = Add Appointment Tests = =
    @Test
    public void testAddAppointmentValid() {
        AppointmentService service = new AppointmentService();
        Date future = new Date(System.currentTimeMillis() + 60_000);

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

    @Test(expected = IllegalArgumentException.class)
    public void testDeleteAppointmentNonExistent() {
        AppointmentService service = new AppointmentService();
        service.deleteAppointment("ZZZZZZZZZZ");
    }

    // = = Next Appointment Tests = =
    @Test
    public void testGetNextAppointmentReturnsEarliestAppointment() {
        AppointmentService service = new AppointmentService();

        Calendar calendar = Calendar.getInstance();

        calendar.add(Calendar.DAY_OF_YEAR, 10);
        Date laterDate = calendar.getTime();

        calendar = Calendar.getInstance();
        calendar.add(Calendar.DAY_OF_YEAR, 5);
        Date earlierDate = calendar.getTime();

        service.addAppointment(laterDate, "Later appointment");
        service.addAppointment(earlierDate, "Earlier appointment");

        Appointment nextAppointment = service.getNextAppointment();

        assertNotNull(nextAppointment);
        assertEquals("Earlier appointment", nextAppointment.getDescription());
    }

    // = = Chronological Ordering Tests = =
    @Test
    public void testGetAppointmentsChronologically() {
        AppointmentService service = new AppointmentService();

        Calendar calendar = Calendar.getInstance();

        calendar.add(Calendar.DAY_OF_YEAR, 2);
        Date firstDate = calendar.getTime();

        calendar = Calendar.getInstance();
        calendar.add(Calendar.DAY_OF_YEAR, 5);
        Date secondDate = calendar.getTime();

        calendar = Calendar.getInstance();
        calendar.add(Calendar.DAY_OF_YEAR, 10);
        Date thirdDate = calendar.getTime();

        service.addAppointment(thirdDate, "Third");
        service.addAppointment(firstDate, "First");
        service.addAppointment(secondDate, "Second");

        List<Appointment> appointments = service.getAppointmentsChronologically();

        assertEquals(3, appointments.size());
        assertEquals("First", appointments.get(0).getDescription());
        assertEquals("Second", appointments.get(1).getDescription());
        assertEquals("Third", appointments.get(2).getDescription());
    }

    // = = Date Range Tests = =
    @Test
    public void testGetAppointmentsBetweenReturnsAppointmentsInRange() {
        AppointmentService service = new AppointmentService();

        Calendar calendar = Calendar.getInstance();

        calendar.add(Calendar.DAY_OF_YEAR, 2);
        Date firstDate = calendar.getTime();

        calendar = Calendar.getInstance();
        calendar.add(Calendar.DAY_OF_YEAR, 5);
        Date secondDate = calendar.getTime();

        calendar = Calendar.getInstance();
        calendar.add(Calendar.DAY_OF_YEAR, 8);
        Date thirdDate = calendar.getTime();

        service.addAppointment(firstDate, "Before range");
        service.addAppointment(secondDate, "Inside range");
        service.addAppointment(thirdDate, "After range");

        Calendar start = Calendar.getInstance();
        start.add(Calendar.DAY_OF_YEAR, 4);

        Calendar end = Calendar.getInstance();
        end.add(Calendar.DAY_OF_YEAR, 6);

        List<Appointment> appointments =
                service.getAppointmentsBetween(start.getTime(), end.getTime());

        assertEquals(1, appointments.size());
        assertEquals("Inside range", appointments.get(0).getDescription());
    }

    @Test(expected = IllegalArgumentException.class)
    public void testGetAppointmentsBetweenRejectsNullStartDate() {
        AppointmentService service = new AppointmentService();

        Calendar calendar = Calendar.getInstance();
        calendar.add(Calendar.DAY_OF_YEAR, 5);

        service.getAppointmentsBetween(null, calendar.getTime());
    }

    @Test(expected = IllegalArgumentException.class)
    public void testGetAppointmentsBetweenRejectsReversedDates() {
        AppointmentService service = new AppointmentService();

        Calendar start = Calendar.getInstance();
        start.add(Calendar.DAY_OF_YEAR, 10);

        Calendar end = Calendar.getInstance();
        end.add(Calendar.DAY_OF_YEAR, 5);

        service.getAppointmentsBetween(start.getTime(), end.getTime());
    }

    // = = Data Structure Synchronization Test = =
    @Test
    public void testDeleteAppointmentRemovesFromAllDataStructures() {
        AppointmentService service = new AppointmentService();

        Calendar calendar = Calendar.getInstance();
        calendar.add(Calendar.DAY_OF_YEAR, 5);

        service.addAppointment(calendar.getTime(), "Appointment to delete");

        Appointment appointment = service.getNextAppointment();
        String id = appointment.getAppointmentId();

        service.deleteAppointment(id);

        assertNull(service.getAppointment(id));
        assertNull(service.getNextAppointment());
        assertTrue(service.getAppointmentsChronologically().isEmpty());
    }
}