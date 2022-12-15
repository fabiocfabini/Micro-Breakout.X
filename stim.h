#ifndef STIM_H
#define	STIM_H

/******************************************************
* TRANSDUCER INTERFACE MODULE *
*******************************************************/

#include <stdint.h>
#include <stdbool.h>

/****************
* PUTCH & GETCH *
*****************/

void putch(uint8_t byte);
uint8_t getch(void);

#define TEDS_IMPLEMENTATION
#include "teds.h"

// Classes & functions
#define COMMON_CMD   1
    #define READ_TEDS_SEG 2
#define XDCR_OPERATE 3
    #define READ_TC_SEG 1
    #define WRITE_TC_SEG 2

#define DATABUFFER_CAP 255
typedef uint8_t DataBuffer[DATABUFFER_CAP];
typedef struct {
    uint8_t dtcn_msb;
    uint8_t dtcn_lsb;
    uint8_t cmd_class;
    uint8_t func;
    uint8_t length_msb;
    uint8_t length_lsb;
} NCAP_cmd;
typedef struct {
    uint8_t stcn_msb;
    uint8_t stcn_lsb;
    uint8_t cmd_class;
    uint8_t func;
    uint8_t length_msb;
    uint8_t length_lsb;
} STIM_cmd;
typedef struct {
    uint8_t res_code;
    uint8_t length_msb;
    uint8_t length_lsb;
} STIM_res;


/*
 * @brief This function reads from, the serial port, the bytes associateed with a ncap command and stores them in a global ncap command struct.
*/
void read_ncap_cmd(void);

/*
 * @brief This function starts an ADC conversion and stores its result in the global data buffer.
 *        It then returns the STIM response code from USART with the retrieved result.
 * @param channel The channel from witch to read the value.
*/
void read_and_send_adc_value(uint8_t channel);

/*
 * @brief This function reads the current value of a LED.
 * @param channel The channel from where to read the LEAD.
*/
void read_from_led(uint8_t channel);

/*
 * @brief This function writes a given value to a LED.
 * @param channel The channel where to write the value.
 * @param value The value to write. ????? DO WE HAVE TO DIFFERENTIATE BETWEEN WRITTING TO A LED OR TO A DIFFERENT ACTUATOR?
*/
void write_to_led(uint8_t channel, bool value);

/*
 * @brief This function interprets the ncap command and acts accordingly.
*/
void interpret_ncap_cmd(void);

/*
 * @brief This function responds to the previously received ncap command with the appropriate data.
 * @param res_code The response code. 0 is interpreted as an error by the ncap.
 * @param length_msb The most significant byte of the length of the response.
 * @param res_code The least significant byte of the length of the response.
 */
void send_stim_response(uint8_t res_code, uint8_t length_msb, uint8_t length_lsb);

#ifdef STIM_IMPLEMENTATION

#define CHAN_POTEN_ADC 0 // RA0
#define CHAN_ACC_X_ADC 8 // RB0
#define CHAN_ACC_Y_ADC 9 // RB1

static NCAP_cmd cmd;
DataBuffer data;
uint8_t adc_result, RESULT_READY;

void read_ncap_cmd(){
    cmd.dtcn_msb = getch();
    cmd.dtcn_lsb = getch();
    cmd.cmd_class = getch();
    cmd.func = getch();
    cmd.length_msb = getch();
    cmd.length_lsb = getch();
    for(uint8_t i = 0; i < cmd.length_lsb + cmd.length_msb*2; i++){
        data[i] = getch();
    }
    
    return;
}

void read_and_send_adc_value(uint8_t channel){
    switch(channel){ // Select ADPCH
        case CHAN_ACC_X:
            ADPCH = CHAN_ACC_X_ADC;
            break;
        case CHAN_ACC_Y:
            ADPCH = CHAN_ACC_Y_ADC;
            break;
        case CHAN_POTEN:
            ADPCH = CHAN_POTEN_ADC;
            break;
        default:
            send_stim_response(0,0,0);
            return;
    }
    
    for(int i = 0; i < 1000; i++);
    
    ADCON0bits.ADGO = 1; // Start conversion
    
    while(!PIR1bits.ADIF); // Wait for conversion to end
    PIR1bits.ADIF = 0;
    data[0] = ADRESH;

    send_stim_response(1,0,1);
    
    return;
}

void read_from_led(uint8_t channel){
    switch(channel){
        case CHAN_LED_RA6:
            data[0] = PORTAbits.RA6; // Read directly from RA port
            send_stim_response(1,0,1);
            return;
        case CHAN_LED_RA7:
            data[0] = PORTAbits.RA7;
            send_stim_response(1,0,1);
            return;
        default:
            send_stim_response(0,0,0);
            return;
    }
}

void write_to_led(uint8_t channel, bool value){
    switch(channel){
        case 3:
            LATAbits.LATA6 = value; // Writing to LATAx. It then will write to RAx
            send_stim_response(1,0,0);
            return;
        case 4:
            LATAbits.LATA7 = value;
            send_stim_response(1,0,0);
            return;
        default:
            send_stim_response(0,0,0);
            return;
    }
}

void interpret_ncap_cmd(){
    read_ncap_cmd();
    switch(cmd.cmd_class){
        case COMMON_CMD:
            switch (cmd.func){
                case READ_TEDS_SEG:
                    switch (data[0]){
                        case META_TEDS_ID:
                            send_meta_teds();
                            return;
                        case TRANSDUCER_TEDS_ID:
                            switch(cmd.dtcn_lsb){
                                case CHAN_ACC_X:
                                    send_tc_teds(CHAN_ACC_X);
                                    return;
                                case CHAN_ACC_Y:
                                    send_tc_teds(CHAN_ACC_Y);
                                    return;
                                case CHAN_POTEN:
                                    send_tc_teds(CHAN_POTEN);
                                    return;
                                case CHAN_LED_RA6:
                                    send_tc_teds(CHAN_LED_RA6);
                                    return;
                                case CHAN_LED_RA7:
                                    send_tc_teds(CHAN_LED_RA7);
                                    return;
                                default:
                                    send_stim_response(0,0,0);
                                    return;
                            }
                            return;
                        default:
                            send_stim_response(0,0,0);
                            return;
                    }
                    return;
                default:
                    send_stim_response(0,0,0);
                    return;
            }
            return;
        case XDCR_OPERATE:
            switch (cmd.func){
                case READ_TC_SEG:
                    switch (cmd.dtcn_lsb){
                        case CHAN_ACC_X:
                            read_and_send_adc_value(CHAN_ACC_X);
                            return;
                        case CHAN_ACC_Y:
                            read_and_send_adc_value(CHAN_ACC_Y);
                            return;
                        case CHAN_POTEN:
                            read_and_send_adc_value(CHAN_POTEN);
                            return;
                        case CHAN_LED_RA6:
                            read_from_led(CHAN_LED_RA6);
                            return;
                        case CHAN_LED_RA7:
                            read_from_led(CHAN_LED_RA7);
                            return;
                        default:
                            send_stim_response(0,0,0);
                            return;
                    }
                    return;
                case WRITE_TC_SEG:
                    switch (cmd.dtcn_lsb){
                        case CHAN_LED_RA6:
                            // write to Led 5
                            write_to_led(cmd.dtcn_lsb, (bool) data[1]);
                            return;
                        case CHAN_LED_RA7:
                            // write to Led 5
                            write_to_led(cmd.dtcn_lsb, (bool) data[1]);
                            return;
                        default:
                            send_stim_response(0,0,0);
                            return;
                    }
                    return;
                default:
                    send_stim_response(0,0,0);
                    return;
            }
            return;
        default:
            send_stim_response(0,0,0);
            return;
    }
}

void send_stim_response(uint8_t res_code, uint8_t length_msb, uint8_t length_lsb){
    putch(res_code); // error code
    putch(length_msb); // length msb
    putch(length_lsb); // length lsb
    
    for(uint8_t i = 0; i < length_lsb; i++){
        putch(data[i]);
    }
    
    return;
}


#endif // STIM_IMPLEMENTATION

#endif	// STIM_H
