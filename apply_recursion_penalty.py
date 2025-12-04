#!/usr/bin/env python3

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
