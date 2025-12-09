Hello,

Throughout this term, I have developed a collection of scripts designed to streamline the grading workflow and make the process more efficient for both graders and ISA staff. Among these, there are two major contributions:

  1. Automated Examples and Tests Grading: A system that automatically assigns grades for examples and test cases, significantly reducing manual effort.
  2. Unified Assignment Processing Script: A consolidated tool that integrates all commonly used grading utilities into a single script, allowing graders to run every required operation for an assignment with one command.

In addition to these larger projects, I have also created several targeted utilities that have provided direct support to ISAs during marking:

  1. Automatic Recursion Penalty Application: Automatically assigns a grade of zero when recursion is detected in assignments where it is not permitted.
  2. Detection of Disallowed Function Usage: Generates a list of students who used specific prohibited functions that may not be caught by existing scripts.
  3. Filtering for Improper Use of Non-Local Functions: Efficiently filters large student .txt files to identify cases where functions were improperly used outside a local scope (relevant for A07 and onward).
  4. Removal of -student Solutions: Deletes all -student solutions which are either the ISA solutions or the instructor solutions that are not to be marked by the TA's/graders saving them submissions.
  5. Detected Recursion in Student Submissions: Updated the already made recursion-hk.py script to detect nested defines + functions within local scope that use recursion. 
     
I will continue to expand this set of tools as the term progresses
