"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """Return the systolic readings stored in encounter records."""
    readings = []
    for encounter in encounters:
        readings.append(encounter["systolic"])
    return readings


def mean_systolic(readings):
    """Return the average of a list of systolic readings, or None if the list is empty."""
    if not readings:
        return None
    return sum(readings) / len(readings)


def count_patients(encounters):
    """Return the number of distinct patients in a list of encounter records."""
    patient_ids = []
    for encounter in encounters:
        patient_ids.append(encounter["patient_id"])
    return len(set(patient_ids))


def patients_at_or_above(encounters, cutoff):
    """Return a list of patient IDs whose systolic readings are at or above the cutoff."""
    patient_ids = []
    for encounter in encounters:
        if encounter["systolic"] >= cutoff:
            patient_ids.append(encounter["patient_id"])
    return list(set(patient_ids))
