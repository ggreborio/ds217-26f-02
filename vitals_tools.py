"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """Creates and returns a list of systolic readings from the encounters."""
    readings = []
    for encounter in encounters:
        readings.append(encounter["systolic"])
    return readings


def mean_systolic(readings):
    """Returns the mean of systolic readings."""
    if not readings:
        return None
    mean = sum(readings) / len(readings)  
    return mean


def count_patients(encounters):
    """Parses the encounters to a set and returns a count of distinct patients."""
    patients = set()
    for encounter in encounters:
        patients.add(encounter["patient_id"])
    return len(patients)


def patients_at_or_above(encounters, cutoff):
    """Returns a set of patient IDs with systolic readings that are at or above the cutoff."""
    patients_above = set()
    for encounter in encounters:
        if encounter["systolic"] >= cutoff:
            patients_above.add(encounter["patient_id"])
    return patients_above
