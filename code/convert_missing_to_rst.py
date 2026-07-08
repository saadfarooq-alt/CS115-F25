#!/usr/bin/env python3

# Sa'ad Farooq (Fall 2025, s4farooq@uwaterloo.ca)
# This script reads a missing_tests.txt file and automatically generates
#     per-student OUTPUT.txt files (RST-style) indicating how many tests
#     each student passed. This is mainly used for assignments where a
#     separate testing pipeline outputs the *number of missing tests*
#     rather than the number of passed tests.
#
# The missing_tests.txt file must contain lines formatted as:
#     <student_id>: Total missing tests: <number>
#
# For each student, this script:
#     - calculates passed_tests = total_tests - missing_tests
#     - creates a directory called missing_autotests where each 
#       student has a folder with an OUTPUT.txt file.
#     - writes an OUTPUT.txt file with the appropriate RST question line:
#
#           Some header info
#
#            ** Question missing: 11/19
#
#           Some footer text
#
# Usage:
#     python3 generate_missing_test_results.py --missing missing_tests.txt --out-results-dir missing_autotests --total-tests 20
#
# Notes:
#     - The --missing file is produced by your test runner or evaluation
#       pipeline that counts how many tests a student did *not* pass.
#     - The --total-tests must be changed for the total number of tests intsturctors want 
#       for the assignment. 
#     - Student folders are created automatically if they do not exist.

import os
import argparse

def parse_missing_file(path):
    """Parse missing_tests.txt into a dictionary {student_id: missing_count}"""
    missing = {}
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(": Total missing tests:")
            if len(parts) != 2:
                continue
            student, count = parts
            missing[student.strip()] = int(count.strip())
    return missing

def write_rst_output(out_dir, student, passed_tests, total_tests, qname="missing"):
    """Create OUTPUT.txt for one student in the correct folder with header/footer"""
    student_dir = os.path.join(out_dir, student)
    os.makedirs(student_dir, exist_ok=True)
    output_file = os.path.join(student_dir, 'OUTPUT.txt')

    with open(output_file, 'w') as f:
        f.write("Some header info\n\n")
        f.write(f" ** Question {qname}: {passed_tests}/{total_tests}\n")
        f.write("\nSome footer text\n")

def main():
    parser = argparse.ArgumentParser(description="Convert missing_tests.txt into RST OUTPUT.txt showing passed tests")
    parser.add_argument('--missing', required=True, help="Path to missing_tests.txt")
    parser.add_argument('--out-results-dir', required=True, help="Folder to write OUTPUT.txt files")
    parser.add_argument('--total-tests', type=int, required=True, help="Total number of tests for this assignment")
    parser.add_argument('--qname', default='missing', help="RST question name (default: missing)")
    args = parser.parse_args()

    missing_tests = parse_missing_file(args.missing)
    out_dir = args.out_results_dir
    total_tests = args.total_tests
    os.makedirs(out_dir, exist_ok=True)

    for student, missing_count in missing_tests.items():
        passed_tests = max(0, total_tests - missing_count)
        write_rst_output(out_dir, student, passed_tests, total_tests, qname=args.qname)

if __name__ == "__main__":
    main()
