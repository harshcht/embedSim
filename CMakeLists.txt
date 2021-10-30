cmake_minimum_required(VERSION 3.5)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)


SET(SHARED_LIB interface.cpp
			   src/controller.cpp)

add_library(controller SHARED ${SHARED_LIB})