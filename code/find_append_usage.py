#!/usr/bin/env python3

# Sa'ad Farooq (Fall 2025, s4farooq@uwaterloo.ca)
# This script is to find the usage of a certain function in the case that
#     some unallowed functions was accidentally skipped over. In this term
#     we had forgotten to remove the function 'append' from the alloweable 
#     functions list. This script will give you a list of students who used 
#     a function that is not allowed, you will need to go in and reduce their
#     based off of the instructors instructions. 
# Usage:
# python3 find_append_usage.py a0X_autotest 
# Note: The X should be changed to the directory you need to go into it.

import os
import sys

def find_append_in_file(path):
    """Return True if the file contains the string 'append'."""
    if not os.path.exists(path):
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            return "append" in content 
    except:
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 find_append_usage.py a08_autotest")
        sys.exit(1)

    base_dir = sys.argv[1]

    if not os.path.isdir(base_dir):
        print("Directory not found:", base_dir)
        sys.exit(1)

    students = sorted(os.listdir(base_dir))

    for student in students:
        student_dir = os.path.join(base_dir, student)
        if not os.path.isdir(student_dir):
            continue

        used_in = []

        # Check q1, q2, q3
        for q in ["a08q1.rkt", "a08q2.rkt", "a08q3.rkt"]: #Change a0Xqx.rkt for the needed questions
            qpath = os.path.join(student_dir, q)
            if find_append_in_file(qpath):
                used_in.append(q.replace(".rkt", ""))

        # Output one line per student
        if used_in:
            print(f"{student}: {' '.join(used_in)}")
        else:
            print(f"{student}: NONE")

if __name__ == "__main__":
    main()

