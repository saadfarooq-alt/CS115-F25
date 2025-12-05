#!/bin/bash

# Sa'ad Farooq (Fall 2025, s4farooq@uwaterloo.ca)
#
# This script automates the full setup and processing workflow for
# assignment grading on MarkUs. It consolidates several commonly used
# tasks into a single command to streamline the ISA workflow.
#
# The script performs all steps that *can* be safely automated, including:
#   - Running distrst and check-testcases concurrently
#   - Generating the graded assignment file
#   - Uploading grading results to MarkUs
#   - Applying RST-based autograding results
#   - Computing missing test counts and converting them into RST marks
#
# The following steps must still be performed manually, as they cannot be
# reliably automated:
#   - Updating MakeGradedAssignment.py
#   - Updating rubric.csv
#   - Running Moss for plagiarism detection
#   - Assigning markers on MarkUs
#
# Usage:
#     ./all-scripts a0X_autotest
#
# Notes:
#   - Replace "X" with the appropriate assignment number.
#   - This script assumes the standard directory layout used by ISAs,
#     including ~/scripts, ~/handin, and ~/marking.
#   - Log files for distrst and check-testcases are saved to ~/logs/<assignment>.
#   - For assignment 4 and onwards, you must open this script with a text editor 
#     and update "--total-tests" in line 96 to match the instructors total checktests.

set -e  

if [ -z "$1" ]; then
    echo "Usage: $0 <assignment_id> (e.g., a05)"
    exit 1
fi

ASSIGNMENT="$1"
AUTOTEST_DIR="${ASSIGNMENT}_autotest"

LOG_DIR=~/logs/$ASSIGNMENT
mkdir -p "$LOG_DIR"

echo "_____________________________________________________________"
echo "Running distrst and check-testcases concurrently for $ASSIGNMENT..."
echo "Logs will be written to: $LOG_DIR"
echo "_____________________________________________________________"

# --- Run distrst in background and log output ---
{
  echo ">>> Starting distrst for $ASSIGNMENT..."
  distrst -t t -s '*' "$AUTOTEST_DIR" 1 AUTOTESTRESULTS
  echo ">>> distrst finished successfully."
} &> "$LOG_DIR/distrst.log" &
DIST_PID=$!

# --- Run tcs in background and log output ---
{
  echo ">>> Starting check-testcases (tcs) for $ASSIGNMENT..."
  cd "../check-testcases/$ASSIGNMENT" || exit 1
  ./tcs
  echo ">>> tcs finished successfully."
} &> "$LOG_DIR/tcs.log" &
TCS_PID=$!

# --- Wait for both to finish ---
wait $DIST_PID
wait $TCS_PID

echo "_____________________________________________________________"
echo "Both distrst and tcs completed. Logs available in:"
echo "  $LOG_DIR/distrst.log"
echo "  $LOG_DIR/tcs.log"
echo "_____________________________________________________________"

# --- Making the GRADDEDASSIGNMENT.rkt 
cd ~/scripts
echo "Running MakeGradedAssignment.py..."
python3 MakeGradedAssignment.py

cd ~
echo "Uploading grading to MarkUs..."
/u/isg/bin/markus.py upload_marking -o --match "GRADED_ASSIGNMENT.ss" "$ASSIGNMENT" "$HOME/handin/${AUTOTEST_DIR}/"

cd ~
echo "Setting marks in MarkUs using RST results..."
/u/isg/bin/markus.py set_marks_rst "$ASSIGNMENT" "$HOME/marking/$ASSIGNMENT/test.1.AUTOTESTRESULTS" "$HOME/marking/$ASSIGNMENT/rubric_converter.csv" 

cd scripts
python3 count_missing_tests.py "$HOME/handin/$AUTOTEST_DIR" > "$HOME/marking/$ASSIGNMENT/missing_tests.txt"

echo "Setting check test cases mark using RST results..."
python3 convert_missing_to_rst.py --missing "$HOME/marking/$ASSIGNMENT/missing_tests.txt" --out-results-dir "$HOME/marking/$ASSIGNMENT/missing_autotest/" --total-tests 19
/u/isg/bin/markus.py set_marks_rst "$ASSIGNMENT" "$HOME/marking/$ASSIGNMENT/missing_autotest" "$HOME/marking/$ASSIGNMENT/correctness_thresholds.csv"

echo "_____________________________________________________________"
echo "All steps completed for assignment $ASSIGNMENT."
echo "_____________________________________________________________"
