#!/usr/bin/env python3

# Sa'ad Farooq (Fall 2025, s4farooq@uwaterloo.ca)
# This script creates a file in structure of:

# missing_tests.txt:
#     studentUSR: Total missing tests: X
#     studentUSR: Total missing tests: Y
#     studentUSR: Total missing tests: Z
#     ...
# Where X,Y,Z are numbers given from this script. 

# This script reads in all the students GRADDED_ASSIGNMENT.ss files and finds all the "Missing test case" 
#     and counts them up giving outputs of numbers based off those missing. 
# Usage:
# python3 count_missing_tests.py <path_to_autotest_folder> >> <path_to_autotest_folder>/missing_tests.txt
# Note: This will give you a missing_tests.txt file that will be used by 
#     convert_missing_to_rst.py to convert all the missing tests into rst results.
#     You will never need to run this on your own as all-scripts.sh does it for you. 
#     You will need to tell the TA's that when they see a "check-manually" OR a missing file
#     they will need to adjust the students mark. 
# VERY IMPORTANT NOTE: All the checktest-case comments MUST start with "Missing test case" 
#     for this script to work properly. 

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
