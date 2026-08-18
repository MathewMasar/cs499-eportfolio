package AppointmentService;

/*
 * Class AppointmentService manages appointments for three independent
 * service schedules.
 *
 * Provides:
 * : unique appointment creation
 * : one TreeMap schedule for each service
 * : available-slot generation by service and date
 * : business-hour and slot validation
 * : deletion and synchronized collection cleanup
 * : ID lookup, chronological retrieval, and next appointment retrieval
 */

import java.security.SecureRandom;
import java.time.Clock;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.EnumMap;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.TreeMap;

public class AppointmentService {

    // = = Constants = =
    private static final LocalTime OPENING_TIME = LocalTime.of(8, 0);
    private static final LocalTime CLOSING_TIME = LocalTime.of(20, 0);
    private static final String ID_CHARACTERS =
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    private static final int ID_LENGTH = 10;

    // = = Fields = =
    // Supports direct appointment lookup and deletion by unique ID.
    private final HashMap<String, Appointment> appointmentsById =
            new HashMap<>();

    // Gives each service its own independent "chair" and schedule.
    private final EnumMap<ServiceType,
            TreeMap<LocalDateTime, Appointment>> appointmentsByService =
            new EnumMap<>(ServiceType.class);

    // Provides efficient access to the next appointment across all services.
    private final PriorityQueue<Appointment> upcomingAppointments =
            new PriorityQueue<>(
                    Comparator.comparing(Appointment::getStartDateTime));

    private final SecureRandom random = new SecureRandom();
    private final Clock clock;

    // = = Constructors = =
    // Uses the computer's current clock during normal application use.
    public AppointmentService() {
        this(Clock.systemDefaultZone());
    }

    // Allows tests to provide a fixed clock for predictable date/time behavior.
    public AppointmentService(Clock clock) {
        if (clock == null) {
            throw new IllegalArgumentException(
                    "Clock cannot be null.");
        }

        this.clock = clock;

        // Create one chronological TreeMap for each independent service.
        for (ServiceType serviceType : ServiceType.values()) {
            appointmentsByService.put(serviceType, new TreeMap<>());
        }
    }

    // = = Available Slot Generation = =
    public List<LocalTime> getAvailableSlots(
            LocalDate appointmentDate,
            ServiceType serviceType) {

        validateDate(appointmentDate);
        validateServiceType(serviceType);

        List<LocalTime> availableSlots = new ArrayList<>();

        // Begin at opening and move forward using the selected service length.
        LocalTime currentSlot = OPENING_TIME;
        int durationMinutes = serviceType.getDurationMinutes();

        while (!currentSlot
                .plusMinutes(durationMinutes)
                .isAfter(CLOSING_TIME)) {

            LocalDateTime proposedStart =
                    appointmentDate.atTime(currentSlot);

            // Past slots for today should not be offered to the caller.
            if (!proposedStart.isBefore(LocalDateTime.now(clock))
                    && isSlotAvailable(
                            appointmentDate,
                            currentSlot,
                            serviceType)) {

                availableSlots.add(currentSlot);
            }

            currentSlot = currentSlot.plusMinutes(durationMinutes);
        }

        return availableSlots;
    }

    // = = Schedule Appointment = =
    public Appointment scheduleAppointment(
            LocalDate appointmentDate,
            LocalTime startTime,
            ServiceType serviceType,
            String description) {

        validateDate(appointmentDate);
        validateStartTime(startTime);
        validateServiceType(serviceType);
        validateDescription(description);

        // A caller may only schedule a start time generated for the service.
        if (!isValidServiceSlot(startTime, serviceType)) {
            throw new IllegalArgumentException(
                    "Selected time is not a valid slot for this service.");
        }

        LocalDateTime proposedStart =
                appointmentDate.atTime(startTime);

        if (proposedStart.isBefore(LocalDateTime.now(clock))) {
            throw new IllegalArgumentException(
                    "Appointment date and time cannot be in the past.");
        }

        if (!isSlotAvailable(
                appointmentDate,
                startTime,
                serviceType)) {

            throw new IllegalArgumentException(
                    "Selected appointment slot is already booked.");
        }

        String appointmentId = generateAppointmentId();

        Appointment appointment = new Appointment(
                appointmentId,
                appointmentDate,
                startTime,
                serviceType,
                description);

        // Update all indexes together after validation succeeds.
        appointmentsById.put(appointmentId, appointment);

        appointmentsByService
                .get(serviceType)
                .put(appointment.getStartDateTime(), appointment);

        upcomingAppointments.offer(appointment);

        return appointment;
    }

    // = = Delete Appointment = =
    public void deleteAppointment(String appointmentId) {
        if (appointmentId == null || appointmentId.isBlank()) {
            throw new IllegalArgumentException(
                    "Appointment ID cannot be null or blank.");
        }

        Appointment appointment =
                appointmentsById.remove(appointmentId);

        if (appointment == null) {
            throw new IllegalArgumentException(
                    "Appointment ID does not exist.");
        }

        // Remove the appointment from its service-specific TreeMap.
        appointmentsByService
                .get(appointment.getServiceType())
                .remove(appointment.getStartDateTime());

        // PriorityQueue removal is linear but keeps next-item retrieval fast.
        upcomingAppointments.remove(appointment);
    }

    // = = Retrieval Methods = =
    public Appointment getAppointment(String appointmentId) {
        return appointmentsById.get(appointmentId);
    }

    public Appointment getNextAppointment() {
        removeExpiredAppointmentsFromQueue();
        return upcomingAppointments.peek();
    }

    // Returns the next upcoming appointment for one selected service.
    // The service-specific TreeMap keeps appointments in chronological order,
    // so ceilingEntry finds the first appointment at or after the current time.
    public Appointment getNextAppointmentForService(
            ServiceType serviceType) {

        validateServiceType(serviceType);

        LocalDateTime currentDateTime =
                LocalDateTime.now(clock);

        Map.Entry<LocalDateTime, Appointment> nextEntry =
                appointmentsByService
                        .get(serviceType)
                        .ceilingEntry(currentDateTime);

        if (nextEntry == null) {
            return null;
        }

        return nextEntry.getValue();
    }

    public List<Appointment> getAppointmentsForService(
            ServiceType serviceType) {

        validateServiceType(serviceType);

        return new ArrayList<>(
                appointmentsByService
                        .get(serviceType)
                        .values());
    }

    public List<Appointment> getAppointmentsForDate(
            LocalDate appointmentDate) {

        validateDate(appointmentDate);

        List<Appointment> appointmentsForDate =
                new ArrayList<>();

        // Gather appointments from all three independent service schedules.
        for (TreeMap<LocalDateTime, Appointment> serviceSchedule
                : appointmentsByService.values()) {

            LocalDateTime startOfDay =
                    appointmentDate.atStartOfDay();
            LocalDateTime startOfNextDay =
                    appointmentDate.plusDays(1).atStartOfDay();

            appointmentsForDate.addAll(
                    serviceSchedule
                            .subMap(
                                    startOfDay,
                                    true,
                                    startOfNextDay,
                                    false)
                            .values());
        }

        appointmentsForDate.sort(
                Comparator.comparing(Appointment::getStartDateTime));

        return appointmentsForDate;
    }

    public List<Appointment> getAppointmentsChronologically() {
        List<Appointment> chronologicalAppointments =
                new ArrayList<>(appointmentsById.values());

        chronologicalAppointments.sort(
                Comparator.comparing(Appointment::getStartDateTime));

        return chronologicalAppointments;
    }

    public Map<String, Appointment> getAllAppointments() {
        // Return a copy so outside code cannot corrupt internal indexes.
        return new HashMap<>(appointmentsById);
    }

    // = = Private Slot Methods = =
    private boolean isValidServiceSlot(
            LocalTime startTime,
            ServiceType serviceType) {

        if (startTime.isBefore(OPENING_TIME)) {
            return false;
        }

        int durationMinutes =
                serviceType.getDurationMinutes();

        if (startTime
                .plusMinutes(durationMinutes)
                .isAfter(CLOSING_TIME)) {

            return false;
        }

        // Slots are measured from 8:00 AM using each service's duration.
        int minutesSinceOpening =
                (startTime.getHour() - OPENING_TIME.getHour()) * 60
                + startTime.getMinute()
                - OPENING_TIME.getMinute();

        return minutesSinceOpening % durationMinutes == 0;
    }

    private boolean isSlotAvailable(
            LocalDate appointmentDate,
            LocalTime startTime,
            ServiceType serviceType) {

        LocalDateTime proposedStart =
                appointmentDate.atTime(startTime);

        // Each service has its own chair, so only the selected service
        // schedule is checked for a conflict.
        return !appointmentsByService
                .get(serviceType)
                .containsKey(proposedStart);
    }

    // = = Private Queue Cleanup = =
    private void removeExpiredAppointmentsFromQueue() {
        LocalDateTime currentDateTime =
                LocalDateTime.now(clock);

        // Remove past appointments from the front until the next one is valid.
        while (!upcomingAppointments.isEmpty()
                && upcomingAppointments
                        .peek()
                        .getStartDateTime()
                        .isBefore(currentDateTime)) {

            upcomingAppointments.poll();
        }
    }

    // = = Private ID Generator = =
    private String generateAppointmentId() {
        String appointmentId;

        do {
            StringBuilder idBuilder =
                    new StringBuilder(ID_LENGTH);

            for (int i = 0; i < ID_LENGTH; i++) {
                int index =
                        random.nextInt(ID_CHARACTERS.length());

                idBuilder.append(
                        ID_CHARACTERS.charAt(index));
            }

            appointmentId = idBuilder.toString();

        } while (appointmentsById.containsKey(appointmentId));

        return appointmentId;
    }

    // = = Private Validation Methods = =
    private void validateDate(LocalDate appointmentDate) {
        if (appointmentDate == null) {
            throw new IllegalArgumentException(
                    "Appointment date cannot be null.");
        }

        if (appointmentDate.isBefore(LocalDate.now(clock))) {
            throw new IllegalArgumentException(
                    "Appointment date cannot be in the past.");
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
                || description.length() > 50) {

            throw new IllegalArgumentException(
                    "Description cannot be null, blank, or longer than 50 characters.");
        }
    }
} // END public class AppointmentService
