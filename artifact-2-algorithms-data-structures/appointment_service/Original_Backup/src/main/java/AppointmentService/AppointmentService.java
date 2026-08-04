package AppointmentService;
/*
 * Class AppointmentService manages Appointment objects.
 * Provides: 
 * : adding appt Unique ID
 * : deleting appt by ID
 */

import java.util.ArrayList;
import java.util.Comparator;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;
import java.util.TreeMap;

public class AppointmentService {

    // = = Fields = =
    // Fast lookup by appointment ID
    private final HashMap<String, Appointment> appointmentsById = new HashMap<>();

    // Automatically maintains appointments in chronological order
    private final TreeMap<Date, List<Appointment>> appointmentsByDate = new TreeMap<>();

    // Efficient retrieval of the next upcoming appointment
    private final PriorityQueue<Appointment> upcomingAppointments =
        new PriorityQueue<>(Comparator.comparing(Appointment::getAppointmentDate));

    // = = Add Appointment = =
    public void addAppointment(Date appointmentDate, String description) {
        String appointmentId;

        do {
            appointmentId = generateAppointmentId();
        } while (appointmentsById.containsKey(appointmentId));

        Appointment appointment = new Appointment(
                appointmentId,
                appointmentDate,
                description);

        // HashMap
        appointmentsById.put(appointmentId, appointment);

        // TreeMap
        appointmentsByDate
                .computeIfAbsent(appointment.getAppointmentDate(),
                        key -> new ArrayList<>())
                .add(appointment);

        // PriorityQueue
        upcomingAppointments.offer(appointment);
    }

    // = = Delete Appointment = =
    public void deleteAppointment(String appointmentId) {

        Appointment appointment = appointmentsById.remove(appointmentId);

        if (appointment == null) {
            throw new IllegalArgumentException(
                    "Appointment ID does not exist.");
        }

        // Remove from TreeMap
        Date date = appointment.getAppointmentDate();

        List<Appointment> appointmentsOnDate =
                appointmentsByDate.get(date);

        appointmentsOnDate.remove(appointment);

        if (appointmentsOnDate.isEmpty()) {
            appointmentsByDate.remove(date);
        }

        // Remove from PriorityQueue
        upcomingAppointments.remove(appointment);
    }

    // = = Retrieve Next Appointment = =
    public Appointment getNextAppointment() {
        return upcomingAppointments.peek();
    }

    // = = Retrieve Appointments Chronologically = =
    public List<Appointment> getAppointmentsChronologically() {
        List<Appointment> chronologicalAppointments = new ArrayList<>();

        for (List<Appointment> appointmentsOnDate : appointmentsByDate.values()) {
            chronologicalAppointments.addAll(appointmentsOnDate);
        }

        return chronologicalAppointments;
    }

    // = = Retrieve Appointments Within Date Range = =
    public List<Appointment> getAppointmentsBetween(Date startDate, Date endDate) {
        if (startDate == null || endDate == null) {
            throw new IllegalArgumentException(
                    "Start date and end date cannot be null.");
        }

        if (startDate.after(endDate)) {
            throw new IllegalArgumentException(
                    "Start date cannot be after end date.");
        }

        List<Appointment> appointmentsInRange = new ArrayList<>();

        appointmentsByDate
                .subMap(startDate, true, endDate, true)
                .values()
                .forEach(appointmentsInRange::addAll);

        return appointmentsInRange;
    }

    // = = Helper: ID Generator = =
    private String generateAppointmentId() {
        String characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        StringBuilder id = new StringBuilder();
        Random random = new Random();

        for (int i = 0; i < 10; i++) {
            // Append a random char from the characters string to build ID
            id.append(characters.charAt(random.nextInt(characters.length())));
        }
        return id.toString();
    }

    // = = Getters for Testing = =
    public Appointment getAppointment(String appointmentId) {
        return appointmentsById.get(appointmentId);
    }

    public HashMap<String, Appointment> getAllAppointments() {
        return appointmentsById;
    }
} // END public class AppointmentService