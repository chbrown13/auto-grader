#include <stdio.h>
#include <dirent.h>
#include "llvm/Support/raw_ostream.h"
#include "llvm/ADT/Statistic.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/Support/Debug.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"
#include "llvm/Support/MemoryBuffer.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/Bitcode/ReaderWriter.h"
#include "llvm/Support/CommandLine.h"
#include "llvm/Pass.h"

using namespace llvm;

static cl::opt<std::string> InputArg("input",
	cl::desc("Specify input filename"),
	cl::Required,
	cl::value_desc("filename"));

/*static cl::opt<std::string> FeedbackType("feedback",
        cl::desc("Specify type of feedback"),
        cl::Required,
        cl::value_desc("user feedback"));*/

bool is_bitcode(const std::string &str) {
			return str.size() >= 3 && str.compare(str.size() - 3, 3, ".bc") == 0;
}

/*Module load_bitcode(const std::string &filename) {
	auto BufferOrError = MemoryBuffer::getFile(filename);
	if(!BufferOrError) {
		errs() << "Cannot load file " << filename << "\n";
		return false;
	}
	else {
		LLVMContext context;
		auto Module = parseBitcodeFile(BufferOrError->get()->getMemBufferRef(), context);
		if(!Module) {
			errs() << "Cannot load module\n";
			return false;
		}
		return Module;
	}
}*/

namespace {
    struct Grade: public ModulePass {
        static char ID;
        Grade(): ModulePass(ID) { }

        bool runOnModule(Module &M) override {
			/*errs() << "In module called: " << M.getName() << "!\n";
			for (auto &F: M) {
			    //F.dump();
				errs() << "In a function called: " << F.getName() << "!\n";
				
				for (auto &B: F) {
					//B.dump();
					errs() << "In a basic block!\n";
		
					for (auto &I: B) {
						//I.dump();
						errs() << "In an instruction!\n";
					}
				}
	    	}*/
	    	const char* input_str = InputArg.c_str();
	    	//std::vector<std::string> files;
	    	if(!is_bitcode(input_str))	
	    	{
				DIR *dir = NULL;
				dir = opendir(input_str);
				struct dirent *input = NULL;
				if(dir == NULL) {
					errs() << "ERROR! Directory could not be initialized correctly";
					exit(3);
				}
				while(input = readdir(dir)) {
					if(input == NULL) {
						errs() << "ERROR! File could not be initialized correctly";
						exit(3);
					}
					if(is_bitcode(input->d_name)) {
						const char* filename = input->d_name;
						printf("%s\n", filename);
						printf("%s\n", input_str);
						//files.insert(filename);
						auto BufferOrError = MemoryBuffer::getFile(filename);
						if(!BufferOrError) {
							errs() << "Cannot load file " << filename << "\n";
						}
						else {
							LLVMContext context;
							auto Module = parseBitcodeFile(BufferOrError->get()->getMemBufferRef(), context);
							if(!Module) {
								errs() << "Cannot load module\n";
							}
							else {
								errs() << "Loaded module " << Module.get().release()->getName() << "!!!\n";
							}
						}
					}
				}
				closedir(dir);
			}
			else {
				auto BufferOrError = MemoryBuffer::getFile(input_str);
				if(!BufferOrError) {
					errs() << "Cannot load file " << input_str << "\n";
				}
				else {
					LLVMContext context;
					auto Module = parseBitcodeFile(BufferOrError->get()->getMemBufferRef(), context);
					if(!Module) {
						errs() << "Cannot load module\n";
					}
					else {
						errs() << "Loaded module " << Module.get().release()->getName() << "!!!\n";
					}
				}
				//files.insert(input_str);
			}
			/*for(i=files.begin(); i<files.end(); i++) {
				errs() << *i << "\n";
			}
		    if(FeedbackType != "student" && FeedbackType != "teacher") {
			errs() << "Invalid Feedback Type! '" << FeedbackType << "'\n";
		    }
		    else {
			    errs() << "feedback type: " << FeedbackType << "\n";
		    }*/
			std::string filename = "/home/chris/Desktop/auto-grader/grade-pass/autograder.py";
			std::string command = "python ";
			command += filename;
			system(command.c_str());

			return false;
		}
    };
}

char Grade::ID = 0;
static RegisterPass<Grade> X("grade", "Auto Grader Pass", false, false);
