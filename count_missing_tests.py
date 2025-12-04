#!/usr/bin/env python3
import os
import re
import sys

def count_missing_tests(filepath):
    """Return the total number of missing test cases in a GRADED_ASSIGNMENT.ss file."""
    total_missing = 0
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if re.match(r'^\d+\.\s+Missing test', line.strip()):
                total_missing += 1
    return total_missing


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 count_missing_tests.py <path_to_autotest_folder>")
        sys.exit(1)

    base_dir = sys.argv[1]

    if not os.path.isdir(base_dir):
        print(f"Error: {base_dir} is not a directory.")
        sys.exit(1)

    student_dirs = sorted(
        [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    )

    for student_name in student_dirs:
        filepath = os.path.join(base_dir, student_name, "GRADED_ASSIGNMENT.ss")
        if os.path.exists(filepath):
            missing_count = count_missing_tests(filepath)
            print(f"{student_name}: Total missing tests: {missing_count}")


if __name__ == "__main__":
    main()
