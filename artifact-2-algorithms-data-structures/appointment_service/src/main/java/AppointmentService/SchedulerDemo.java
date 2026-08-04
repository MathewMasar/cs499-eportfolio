package AppointmentService;

/*
 * Class SchedulerDemo provides a simple console demonstration of the
 * consulting appointment scheduler.
 *
 * Provides:
 * : creation of appointments for each service tier
 * : next appointment retrieval for each individual service
 * : chronological display of all scheduled appointments
 */

import java.time.LocalDate;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

public class SchedulerDemo {

    // = = Display Formatters = =
    private static final DateTimeFormatter DATE_FORMAT =
            DateTimeFormatter.ofPattern("MMMM d, yyyy");

    private static final DateTimeFormatter TIME_FORMAT =
            DateTimeFormatter.ofPattern("h:mm a");

    // = = Main Program = =
    public static void main(String[] args) {

        AppointmentService service =
                new AppointmentService();

        LocalDate appointmentDate =
                LocalDate.now().plusDays(7);

        printHeader();

        // Schedule one appointment for each independent service tier.
        Appointment basicAppointment =
                service.scheduleAppointment(
                        appointmentDate,
                        LocalTime.of(8, 30),
                        ServiceType.BASIC_SERVICE,
                        "Basic consultation");

        Appointment standardAppointment =
                service.scheduleAppointment(
                        appointmentDate,
                        LocalTime.of(8, 45),
                        ServiceType.STANDARD_SERVICE,
                        "Standard consultation");

        Appointment premiumAppointment =
                service.scheduleAppointment(
                        appointmentDate,
                        LocalTime.of(8, 0),
                        ServiceType.PREMIUM_SERVICE,
                        "Premium consultation");

        printScheduledAppointment(basicAppointment);
        printScheduledAppointment(standardAppointment);
        printScheduledAppointment(premiumAppointment);

        printNextAppointmentsByService(service);

        printAllAppointments(service);
    }

    // = = Header Display = =
    private static void printHeader() {
        System.out.println(
                "============================================================");
        System.out.println(
                "          CONSULTING APPOINTMENT SCHEDULER DEMO");
        System.out.println(
                "============================================================");
        System.out.println();
    }

    // = = Scheduled Appointment Display = =
    private static void printScheduledAppointment(
            Appointment appointment) {

        System.out.println("Scheduled:");
        System.out.println(
                "Service     : "
                        + appointment
                                .getServiceType()
                                .getDisplayName());

        System.out.println(
                "Date        : "
                        + appointment
                                .getAppointmentDate()
                                .format(DATE_FORMAT));

        System.out.println(
                "Start Time  : "
                        + appointment
                                .getStartTime()
                                .format(TIME_FORMAT));

        System.out.println(
                "End Time    : "
                        + appointment
                                .getEndDateTime()
                                .toLocalTime()
                                .format(TIME_FORMAT));

        System.out.println(
                "Description : "
                        + appointment.getDescription());

        System.out.println(
                "------------------------------------------------------------");
    }

    // = = Next Appointment Display = =
    private static void printNextAppointmentsByService(
            AppointmentService service) {

        System.out.println();
        System.out.println(
                "============================================================");
        System.out.println(
                "NEXT APPOINTMENTS BY SERVICE");
        System.out.println(
                "============================================================");

        printNextAppointment(
                service,
                ServiceType.BASIC_SERVICE);

        printNextAppointment(
                service,
                ServiceType.STANDARD_SERVICE);

        printNextAppointment(
                service,
                ServiceType.PREMIUM_SERVICE);
    }

    // Displays the next appointment for one selected service tier.
    private static void printNextAppointment(
            AppointmentService service,
            ServiceType serviceType) {

        Appointment appointment =
                service.getNextAppointmentForService(serviceType);

        System.out.println();
        System.out.println(serviceType.getDisplayName());

        if (appointment == null) {
            System.out.println(
                    "No upcoming appointments scheduled.");

            System.out.println(
                    "------------------------------------------------------------");
            return;
        }

        System.out.println(
                "Date        : "
                        + appointment
                                .getAppointmentDate()
                                .format(DATE_FORMAT));

        System.out.println(
                "Start Time  : "
                        + appointment
                                .getStartTime()
                                .format(TIME_FORMAT));

        System.out.println(
                "Description : "
                        + appointment.getDescription());

        System.out.println(
                "------------------------------------------------------------");
    }

    // = = Chronological Appointment Display = =
    private static void printAllAppointments(
            AppointmentService service) {

        List<Appointment> appointments =
                service.getAppointmentsChronologically();

        System.out.println();
        System.out.println(
                "============================================================");
        System.out.println(
                "ALL SCHEDULED APPOINTMENTS");
        System.out.println(
                "============================================================");

        for (Appointment appointment : appointments) {
            System.out.println(
                    appointment
                            .getStartTime()
                            .format(TIME_FORMAT)
                            + " | "
                            + appointment
                                    .getServiceType()
                                    .getDisplayName()
                            + " | "
                            + appointment.getDescription());
        }

        System.out.println(
                "============================================================");
    }
} // END public class SchedulerDemo
