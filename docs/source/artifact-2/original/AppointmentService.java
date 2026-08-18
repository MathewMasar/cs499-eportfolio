package AppointmentService;
/*
 * Class AppointmentService manages Appointment objects.
 * Provides: 
 * : adding appt Unique ID
 * : deleting appt by ID
 */

import java.util.Date;
import java.util.HashMap;
import java.util.Random;

public class AppointmentService {

    // = = Fields = =
    private HashMap<String, Appointment> appointments = new HashMap<>();

    // = = Add Appointment = =
    public void addAppointment(Date appointmentDate, String description) {
        String appointmentId;

        // Generate unique 10 char ID
        do {
            appointmentId = generateAppointmentId();
        } while (appointments.containsKey(appointmentId)); // Repeat until unique ID

        Appointment appt = new Appointment(appointmentId, appointmentDate, description);
        appointments.put(appointmentId, appt);
    }

    // = = Delete Appointment = =
    public void deleteAppointment(String appointmentId) {
        if (!appointments.containsKey(appointmentId)) {
            throw new IllegalArgumentException("Appointment ID does not exist.");
        }
        appointments.remove(appointmentId);
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
        return appointments.get(appointmentId);
    }

    public HashMap<String, Appointment> getAllAppointments() {
        return appointments;
    }
} // END public class AppointmentService