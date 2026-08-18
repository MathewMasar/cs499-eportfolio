package AppointmentService;

/*
 * Enum ServiceType defines the three appointment services offered by
 * the scheduling system. Each service owns an independent schedule
 * and uses a fixed appointment duration.
 */

public enum ServiceType {

    // = = Available Services = =
    BASIC_SERVICE("30-Minute Service", 30),
    STANDARD_SERVICE("45-Minute Service", 45),
    PREMIUM_SERVICE("60-Minute Service", 60);

    // = = Fields = =
    private final String displayName;
    private final int durationMinutes;

    // = = Constructor = =
    ServiceType(String displayName, int durationMinutes) {
        this.displayName = displayName;
        this.durationMinutes = durationMinutes;
    }

    // = = Getters = =
    public String getDisplayName() {
        return displayName;
    }

    public int getDurationMinutes() {
        return durationMinutes;
    }
} // END public enum ServiceType
