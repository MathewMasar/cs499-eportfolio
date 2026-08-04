package AppointmentService;
/*
 * Class Appointment defines object and validates all constraints. 
 * Provides: getter for all fields (all are non updatable)
 */

import java.util.Date;

public class Appointment {

    // = = Fields = =
    private final String appointmentId;   // Cannot change after creation
    private final Date appointmentDate;   // Must not be in the past, not null
    private final String description;     // Required, <= 50 chars

    // = = Constructor = =
    public Appointment(String appointmentId, Date appointmentDate, String description) {
        validateAppointmentId(appointmentId);
        validateAppointmentDate(appointmentDate);
        validateDescription(description);

        this.appointmentId = appointmentId;
        // Copy to prevent external modification, Date util is mutable
        this.appointmentDate = new Date(appointmentDate.getTime());
        this.description = description;
    }

    // = = Getters (all fields) = =
    public String getAppointmentId() {
        return appointmentId;
    }

    public Date getAppointmentDate() {
        // Return copy
        return new Date(appointmentDate.getTime());
    }

    public String getDescription() {
        return description;
    }

    // = = Private Validation Methods = =
    private void validateAppointmentId(String appointmentId) {
        // ID cannot be null or longer than 10 char
        if (appointmentId == null || appointmentId.length() > 10) {
            throw new IllegalArgumentException("Appointment ID cannot be null or longer than 10 characters.");
        }
    }

    private void validateAppointmentDate(Date date) {
        // Date cannot be null or in the past
        if (date == null || date.before(new Date())) {
            throw new IllegalArgumentException("Appointment date cannot be null or in the past.");
        }
    }

    private void validateDescription(String description) {
        // Description cannot be null or longer than 50 char
        if (description == null || description.length() > 50) {
            throw new IllegalArgumentException("Description cannot be null or longer than 50 characters.");
        }
    }
} // END public class Appointment