# Auto-Grader

CSC791: Automated Program Repair, Independent Study with Guoliang Jin

This project examines the impact of integrating automated program repair in computer science education. I developed a new project grading algorithm based on generated patches and evaluated it on introductory programming assignments from the [IntroClass](https://github.com/ProgramRepair/IntroClass) program repair benchmark. More details and my findings can be found in paper/project.pdf.

### Instructions to run patch grading tool:

* git clone https://github.ncsu.edu/chbrown13/auto-grader.git
* git clone https://github.com/ProgramRepair/IntroClass.git (Follow instructions to build and make [IntroClass](https://github.com/ProgramRepair/IntroClass))
* cd IntroClass/
* make
* cd ..
* cd auto-grader/
* git checkout -b CSC791
* Change the first line in grade_utils.py to make BASE_PATH the path where IntroClass is stored locally
* Change Line 12 of autograder.py to set BUGHUNT to the location where the [SearchRepair](https://github.com/ProgramRepair/SearchRepair) results are stored (Patches not available to public)
* python autograder.py


### Repository Structure

```
auto-grader/
 |-paper/
 |----paper.pdf (Final report for CSC791 class)
 |-results/
 |----checksum/
 |--------08c7e.txt
 |--------... (output files generated for each student containing no patch, automated patch, and human patch grades for each submission)
 |--------grades.csv (csv file of all the grades calculated)
 |--------project_data.csv (output containing grading data for the entire project i.e. average grade, number of each letter grade, etc.)
 |----digits/
 |----... (rest of IntroClass projects)
 |-README.md (This document)
 |-autograder.py (main python script)
 |-grade_utils.py (functions for patch grading formula implementation)
 |-patch.py (defines a patch)
 |-student.py (defines a student)
```
