# auto-grader
LLVM Pass to automatically repair and grade student programming assignments

###Branches
- [master](https://github.ncsu.edu/dcbrow10/auto-grader/tree/master): _Main branch for the tool and future work_
- [CSC791](https://github.ncsu.edu/dcbrow10/auto-grader/tree/CSC791): _Automated Program Repair class final project_

To run tool:
* git clone https://github.ncsu.edu/dcbrow10/auto-grader.git
* cd auto-grader
* mkdir build
* cd build
* cmake ..
* make
* cd ..
* opt -load build/grade-pass/libGradePass.so -grade -input=[input_file].bc [file].bc
