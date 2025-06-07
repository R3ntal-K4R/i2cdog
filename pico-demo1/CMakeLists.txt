cmake_minimum_required(VERSION 3.12)

# Pull in PICO SDK (must be before project)
include(pico_sdk_import.cmake)

project(pico_examples C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)


set(PICO_EXAMPLES_PATH ${PROJECT_SOURCE_DIR})


# Initialize the SDK
pico_sdk_init()


add_executable(voltmeter-i2c
        voltmeter-i2c.c
        )

# Pull in our pico_stdlib which pulls in commonly used features
target_link_libraries(voltmeter-i2c pico_stdlib hardware_uart hardware_adc hardware_i2c)

# create map/bin/hex file etc.
pico_add_extra_outputs(voltmeter-i2c)

# add url via pico_set_program_url
#example_auto_set_url(voltmeter-i2c)
