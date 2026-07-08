#!/usr/bin/env python3

# Sa'ad Farooq (Fall 2025, s4farooq@uwaterloo.ca)
# This script will automatically set grades to 0 for students who use recrusion
#     this only applies to A08 unless there are other assignments where you need to give 
#     students 0's for recursion.
# Usage:
# python3 apply_recursion_penalty.py output.txt <shorthand_name_of_assignment_on_markus>
# Note: the output.txt is given from python ./recursion-hk.py */*.rkt > output.txt. Also
#     if there is only one question you need to look for recurison on use this output.txt file:
#     python ./recursion-hk.py */a0Xqx.rkt > output.txt. Where X is the assignment name and x is 
#     the question you need to check.

import sys
import subprocess
import re

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 apply_recursion_penalty.py output.txt assignment_name")
        sys.exit(1)

    input_file = sys.argv[1]
    assignment_name = sys.argv[2]

    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if "contains recursive functions:" not in line:
                continue

            # Remove "***"
            if line.startswith("***"):
                line = line[3:].lstrip()

            # Extract student + filename
            student_path, _ = line.split(" contains recursive functions:")
            student, question_file = student_path.split("/")

            # question_file example: a08q2.rkt → extract q2 → 2
            match = re.search(r"q([0-9]+)", question_file)
            if not match:
                print("Could not extract question number from:", question_file)
                continue

            qnum = match.group(1)  # ONLY the question number

            criterion_name = f"Q{qnum} Correctness"

            cmd = [
                "/u/isg/bin/markus.py",
                "set_mark",
                assignment_name,
                student,
                criterion_name,
                "0"
            ]

            print("Running:", ' '.join(cmd))
            subprocess.run(cmd)

if __name__ == "__main__":
    main()
