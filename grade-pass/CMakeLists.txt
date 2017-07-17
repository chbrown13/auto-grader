add_library(GradePass MODULE Grade.cpp)

target_compile_features(GradePass PRIVATE cxx_range_for cxx_auto_type)

set_target_properties(GradePass PROPERTIES COMPILE_FLAGS "-fno-rtti")

if(APPLE)
	set_target_properties(GradePass PROPERTIES
		 LINK_FLAGS "-undefined dynamic_lookup")
endif(APPLE)
