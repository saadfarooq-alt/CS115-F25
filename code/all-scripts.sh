#!/bin/bash

# Sa'ad Farooq (Fall 2025, s4farooq@uwaterloo.ca)
#
# This script automates the full setup and processing workflow for
# assignment grading on MarkUs. It consolidates several commonly used
# tasks into a single command to streamline the ISA workflow.
#
# The script performs all steps that *can* be safely automated, including:
#   - Running distrst and check-testcases concurrently (if assignments >= a04 check-testcases are run aswell)
#   - Generating the graded assignment file
#   - Uploading grading results to MarkUs
#   - Applying RST-based autograding results
#   - Computing missing test counts and converting them into RST marks (if assignments >= a04)
#
# The following steps must still be performed manually:
#   - Updating MakeGradedAssignment.py
#   - Updating rubric.csv
#   - Running Moss
#   - Assigning markers on MarkUs
#
# Usage:
#     ./all-scripts <assignment_id>

set -e  

if [ -z "$1" ]; then
    echo "Usage: $0 <assignment_id> (e.g., a05)"
    exit 1
fi

ASSIGNMENT="$1"
AUTOTEST_DIR="${ASSIGNMENT}_autotest"

# --- Extract numeric assignment number ---
ASSIGN_NUM=$(echo "$ASSIGNMENT" | sed 's/[^0-9]*//g')

LOG_DIR=~/logs/$ASSIGNMENT
mkdir -p "$LOG_DIR"

echo "_____________________________________________________________"
echo "Running distrst for $ASSIGNMENT..."
echo "_____________________________________________________________"

# Always run distrst
{
  distrst -t t -s '*' "$AUTOTEST_DIR" 1 AUTOTESTRESULTS
} &> "$LOG_DIR/distrst.log" &
DIST_PID=$!

# ------------------------------------------------------------
# Run tcs ONLY if assignment number >= 4
# ------------------------------------------------------------
if [ "$ASSIGN_NUM" -ge 4 ]; then
    echo "Assignment $ASSIGNMENT is >= a04 — running check-testcases..."
    {
      cd "../check-testcases/$ASSIGNMENT" || exit 1
      ./tcs
    } &> "$LOG_DIR/tcs.log" &
    TCS_PID=$!
else
    echo "Assignment $ASSIGNMENT is < a04 — skipping check-testcases."
    TCS_PID=""
fi

# Wait for distrst
wait $DIST_PID

# Wait for tcs only if it was run
if [ -n "$TCS_PID" ]; then
    wait $TCS_PID
fi

echo "_____________________________________________________________"
echo "Finished core testing steps."
echo "_____________________________________________________________"

# --- Making the GRADDEDASSIGNMENT.rkt 
cd ~/scripts
python3 MakeGradedAssignment.py

cd ~
/u/isg/bin/markus.py upload_marking -o --match "GRADED_ASSIGNMENT.ss" "$ASSIGNMENT" "$HOME/handin/${AUTOTEST_DIR}/"

/u/isg/bin/markus.py set_marks_rst "$ASSIGNMENT" "$HOME/marking/$ASSIGNMENT/test.1.AUTOTESTRESULTS" "$HOME/marking/$ASSIGNMENT/rubric_converter.csv"

# ------------------------------------------------------------
# Missing test checks ONLY for assignments >= a04
# ------------------------------------------------------------
if [ "$ASSIGN_NUM" -ge 4 ]; then
    echo "Assignment >= a04 — computing missing test penalties..."

    cd scripts
    python3 count_missing_tests.py "$HOME/handin/$AUTOTEST_DIR" > "$HOME/marking/$ASSIGNMENT/missing_tests.txt"

    python3 convert_missing_to_rst.py \
        --missing "$HOME/marking/$ASSIGNMENT/missing_tests.txt" \
        --out-results-dir "$HOME/marking/$ASSIGNMENT/missing_autotest/" \
        --total-tests 19

    /u/isg/bin/markus.py set_marks_rst \
        "$ASSIGNMENT" \
        "$HOME/marking/$ASSIGNMENT/missing_autotest" \
        "$HOME/marking/$ASSIGNMENT/correctness_thresholds.csv"

else
    echo "Assignment < a04 — skipping missing test penalties."
fi

echo "_____________________________________________________________"
echo "All steps completed for assignment $ASSIGNMENT."
echo "_____________________________________________________________"
