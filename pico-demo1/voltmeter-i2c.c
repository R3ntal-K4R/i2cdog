/**
 * Raspberry Pi Pico - Voltmeter
 * Sends via i2c
 * Works with ADC pin 0
 * See: www.penguintutor.com/projects/pico
 */


#include "pico/stdlib.h"
#include "hardware/uart.h"
#include "hardware/adc.h"
#include "hardware/i2c.h"
#include <stdio.h>


/// \tag::voltmeter-i2c[]

#define UART_ID uart1
#define BAUD_RATE 115200
#define DATA_BITS 8
#define STOP_BITS 1
#define PARITY    UART_PARITY_NONE

// UART pins
#define UART_TX_PIN 4
#define UART_RX_PIN 5

#define I2C_ADDR 0x3E

// Whch pin to monitor - default to 0
static int adc_pin = 0;

// conversion factor is into mili volts
const float conversion_factor=3.3f*1000/(1<<12);


int main() {
    // setup ADC
    stdio_init_all();
    adc_init();
    // set gpio as adc (no_pullups etc)
    adc_gpio_init(26);
    adc_select_input(adc_pin);

    // Set up UART (debugging)
    // Set up our UART with a basic baud rate.
    uart_init(UART_ID, 2400);
    // Set the TX and RX pins by using the function select on the GPIO
    // Set datasheet for more information on function select
    gpio_set_function(UART_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(UART_RX_PIN, GPIO_FUNC_UART);
    int actual = uart_set_baudrate(UART_ID, BAUD_RATE);
    // Set UART flow control CTS/RTS, we don't want these, so turn them off
    uart_set_hw_flow(UART_ID, false, false);
    // Set our data format
    uart_set_format(UART_ID, DATA_BITS, STOP_BITS, PARITY);
    // Turn off FIFO's - we want to do this character by character
    uart_set_fifo_enabled(UART_ID, false);

    // i2c setup
    i2c_init(i2c1, 10000);
    i2c_set_slave_mode(i2c1, true, I2C_ADDR);
    gpio_set_function(2, GPIO_FUNC_I2C);
    gpio_set_function(3, GPIO_FUNC_I2C);
    gpio_pull_up(2);
    gpio_pull_up(3);

    uart_puts(UART_ID, "Voltage-i2c on Pico");
    
    uint8_t rxdata[4];
    uint8_t txdata[2];
    char message[20];
    while (true) {
        // Receive data from controller
        // 3 bytes received - byte 0 is cmd (used as lower byte) byte 2 is higher - byte 3 is 0
           if (i2c_get_read_available(i2c1) < 3) continue;
        i2c_read_raw_blocking (i2c1, rxdata, 3);
        //sprintf (message, "Rx: %d %d %d\r\n", rxdata[0], rxdata[1], rxdata[2]);
        //uart_puts(UART_ID, message);
        sprintf (message, "Value %d\r\n", rxdata[0]+(rxdata[1]<<8));
        uart_puts(UART_ID, message);
        
        // Respond with ADC value (in milivolts)
        uint16_t adc_value=adc_read();
        // Note that this will drop fraction rather than round, but close enough
        int value = (int) adc_value * conversion_factor;
        txdata[0] = value & 0xFF;
        txdata[1] = value >> 8;
        sprintf (message, "Tx: %d %d - %d\r\n", txdata[0], txdata[1], value);
        uart_puts(UART_ID, message);
        // Sends data in mv (as int)
        i2c_write_raw_blocking(i2c1, txdata, 2);
        
    }
}

/// \end:voltmeter-i2c[]
