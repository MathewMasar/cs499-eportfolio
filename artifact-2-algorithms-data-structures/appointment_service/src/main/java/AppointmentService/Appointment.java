package AppointmentService;

/*
 * Class Appointment defines one scheduled appointment.
 *
 * Provides:
 * : immutable appointment data
 * : validation of required fields
 * : calculated start and end date/time values
 * : defensive design through immutable java.time classes
 */

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.Objects;

public class Appointment {

    // = = Constants = =
    private static final int MAX_ID_LENGTH = 10;
    private static final int MAX_DESCRIPTION_LENGTH = 50;

    // = = Fields = =
    private final String appointmentId;
    private final LocalDate appointmentDate;
    private final LocalTime startTime;
    private final ServiceType serviceType;
    private final String description;

    // = = Constructor = =
    public Appointment(
            String appointmentId,
            LocalDate appointmentDate,
            LocalTime startTime,
            ServiceType serviceType,
            String description) {

        validateAppointmentId(appointmentId);
        validateAppointmentDate(appointmentDate);
        validateStartTime(startTime);
        validateServiceType(serviceType);
        validateDescription(description);

        this.appointmentId = appointmentId;
        this.appointmentDate = appointmentDate;
        this.startTime = startTime;
        this.serviceType = serviceType;
        this.description = description;
    }

    // = = Getters = =
    public String getAppointmentId() {
        return appointmentId;
    }

    public LocalDate getAppointmentDate() {
        return appointmentDate;
    }

    public LocalTime getStartTime() {
        return startTime;
    }

    public ServiceType getServiceType() {
        return serviceType;
    }

    public String getDescription() {
        return description;
    }

    // Combines the stored date and time for chronological comparisons.
    public LocalDateTime getStartDateTime() {
        return appointmentDate.atTime(startTime);
    }

    // Calculates the appointment end instead of storing duplicate data.
    public LocalDateTime getEndDateTime() {
        return getStartDateTime()
                .plusMinutes(serviceType.getDurationMinutes());
    }

    // = = Private Validation Methods = =
    private void validateAppointmentId(String appointmentId) {
        if (appointmentId == null
                || appointmentId.isBlank()
                || appointmentId.length() > MAX_ID_LENGTH) {

            throw new IllegalArgumentException(
                    "Appointment ID cannot be null, blank, or longer than 10 characters.");
        }
    }

    private void validateAppointmentDate(LocalDate appointmentDate) {
        if (appointmentDate == null) {
            throw new IllegalArgumentException(
                    "Appointment date cannot be null.");
        }
    }

    private void validateStartTime(LocalTime startTime) {
        if (startTime == null) {
            throw new IllegalArgumentException(
                    "Appointment start time cannot be null.");
        }
    }

    private void validateServiceType(ServiceType serviceType) {
        if (serviceType == null) {
            throw new IllegalArgumentException(
                    "Service type cannot be null.");
        }
    }

    private void validateDescription(String description) {
        if (description == null
                || description.isBlank()
                || description.length() > MAX_DESCRIPTION_LENGTH) {

            throw new IllegalArgumentException(
                    "Description cannot be null, blank, or longer than 50 characters.");
        }
    }

    // = = Equality Methods = =
    // Appointment IDs uniquely identify appointments throughout the service.
    @Override
    public boolean equals(Object object) {
        if (this == object) {
            return true;
        }

        if (!(object instanceof Appointment)) {
            return false;
        }

        Appointment other = (Appointment) object;
        return appointmentId.equals(other.appointmentId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(appointmentId);
    }
} // END public class Appointment
