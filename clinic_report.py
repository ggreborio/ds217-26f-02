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
    """One usable encounter is a dictionary with keys "patient_id" and "systolic", in which systolic value is an integer and between 60 and 250.

    Give back two values: the list of usable encounters, and how many data
    rows you skipped. `main()` unpacks them the way the lecture unpacks a
    tuple, with two names on the left of the `=`.
    """
    encounters = []
    skipped = 0
    with open(data_path, "r", encoding="utf-8") as file:
        data = file.readlines()
    for row in data[1:]:
        fields = row.strip().split(",")
        if len(fields) == 3:
            try:
                systolic = int(fields[2])
                if systolic > 250 or systolic < 60:
                    skipped += 1
                    print(f"Row has implausible systolic value: {row.strip()}")
                else:
                    encounters.append({"patient_id": fields[0], "systolic": systolic})
            except ValueError:
                skipped += 1
                print(f"Row has non-integer systolic value: {row.strip()}")
        else:
            skipped += 1
            print(f"Row does not have 3 fields: {row.strip()}")
    return encounters, skipped


def main():
    """Creates one file that reports a statistical summary of the systolic data and a file with the systolic cutoff and patient ID that qualifies for follow-up"""
    encounters, skipped = read_encounters(DATA_PATH)

    with open(OUTPUT_DIR/"vitals_report.txt", "w", encoding="utf-8") as file:
        print(f"Usable encounters: {len(encounters)}", file=file)
        print(f"Skipped rows: {skipped}", file=file)
        print(f"Patients seen: {count_patients(encounters)}", file=file)
        print(f"Mean systolic: {mean_systolic(systolic_readings(encounters)):.1f} mmHg", file=file)
        print(f"Highest systolic: {max(systolic_readings(encounters))} mmHg", file=file)
        print(f"Lowest systolic: {min(systolic_readings(encounters))} mmHg", file=file)
  
    with open(OUTPUT_DIR/"vitals_report.txt", "r", encoding="utf-8") as file:
        print("vitals_report.txt", end="")

    with open(OUTPUT_DIR/"followup_list.txt", "w", encoding="utf-8") as file:
        cutoff = 160
        print(f"Cutoff: {cutoff} mmHg", file=file)
        print("Reason: a higher systolic cutoff will allow clinicians to reduce the amount of patients and increase quality of care", file=file)
        for patient_id in sorted(patients_at_or_above(encounters, cutoff)):
            print(patient_id, file=file)

if __name__ == "__main__":
    main()
