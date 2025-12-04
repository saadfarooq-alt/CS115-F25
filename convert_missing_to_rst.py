#!/usr/bin/env python3
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
