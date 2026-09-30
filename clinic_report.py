#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """Read clinic encounter data and return usable encounters and the number skipped.

    Each usable encounter is a dictionary containing a patient ID, visit date,
    and systolic blood pressure as an integer.
    """
    with open(data_path, "r") as file:
        rows = file.readlines()

    encounters = []
    skipped = 0

    for row in rows[1:]:
        if not row.strip():
            skipped += 1
            print("Skipping a blank row.")
            continue

        fields = row.strip().split(",")

        if len(fields) != 3:
            skipped += 1
            print(f"Skipping a row with {len(fields)} fields: {row.strip()}")
            continue

        patient_id, visit_date, raw_systolic = fields

        try:
            systolic = int(raw_systolic)
        except ValueError as error:
            skipped += 1
            print(f"Skipping {patient_id}: {error}")
            continue

        if systolic < 70 or systolic > 250:
            skipped += 1
            print(f"Skipping {patient_id}: implausible systolic reading {systolic}")
            continue

        encounters.append({
            "patient_id": patient_id,
            "visit_date": visit_date,
            "systolic": systolic,
        })

    return encounters, skipped



def main():
    """Write a vitals summary report and a patient follow-up list."""
    encounters, skipped = read_encounters(DATA_PATH)

    readings = systolic_readings(encounters)

    report_lines = [
        f"Usable encounters: {len(encounters)}",
        f"Skipped rows: {skipped}",
        f"Patients seen: {count_patients(encounters)}",
        f"Mean systolic: {mean_systolic(readings):.1f} mmHg",
        f"Highest systolic: {max(readings)} mmHg",
        f"Lowest systolic: {min(readings)} mmHg",
    ]

    report_text = "\n".join(report_lines) + "\n"

    with open("output/vitals_report.txt", "w") as file:
        file.write(report_text)

    with open("output/vitals_report.txt", "r") as file:
        saved_text = file.read()

    print(saved_text)

    print(f"Saved report matches: {saved_text == report_text}")
    assert saved_text == report_text, "the saved report does not match the text we built"


if __name__ == "__main__":
    main()
