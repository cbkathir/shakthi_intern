cmake_minimum_required(VERSION 2.6)
project(CSPIKESV)

SET(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${bin})
SET(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${bin})
SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${bin})

set(RISCV $ENV{RISCV})

INCLUDE_DIRECTORIES(${RISCV}/include/)
INCLUDE_DIRECTORIES(${RISCV}/lib)
INCLUDE_DIRECTORIES(${RISCV}/../riscv-isa-sim/riscv)
INCLUDE_DIRECTORIES(${RISCV}/../riscv-isa-sim/build)
INCLUDE_DIRECTORIES(${RISCV}/../riscv-isa-sim/softfloat)

SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -Wall -std=c++11")

INCLUDE_DIRECTORIES(./debug_rom/)

link_directories(${RISCV}/lib)

add_library (slsvSpikeIf SHARED SpikeIf.cpp)
target_include_directories (slsvSpikeIf PUBLIC ${CMAKE_CURRENT_SOURCE_DIR} ${RISCV}/include)
target_link_libraries(slsvSpikeIf fesvr)

#add_executable (testing main.c SpikeIf.cpp)
#target_include_directories (testing PUBLIC ${CMAKE_CURRENT_SOURCE_DIR} ${RISCV}/include)
#target_link_libraries(testing fesvr)
