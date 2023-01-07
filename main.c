#include <xc.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define _XTAL_FREQ 32000000   //the clock frequency defined in config() must be provided here for the delay function

#define STIM_IMPLEMENTATION
#include "stim.h"

void config(void);
uint8_t getch(void);
uint8_t echo_rec_bytes(void);
uint8_t echo_single_byte(void);
void __interrupt() int_handler(void); //the interrupt handler routine must be declared as __interrupt(). When an INT happens, this function is called
void putch(uint8_t byte) ; //function used to send data via UART. The printf uses this function too.

void main(void) {
    config();  //this ASM function configures the microcontroller 
    init_meta_teds();
    init_tc_teds();
    
    while(1){
      ;
    }
}

void putch(uint8_t byte) 
{
#ifdef __XC8
    while (!PIR3bits.TX1IF);
    TX1REG = byte;
    while (!PIR3bits.TX1IF);
#else
    printf("%d\n", byte);
#endif
}

uint8_t getch(void){
    RC1STAbits.OERR = 0;    // Would like to test this
    while(!PIR3bits.RC1IF);
    return RC1REG;
}

uint8_t echo_single_byte(void) {
    putch(getch());
    return 0;
}

uint8_t echo_rec_bytes(void) {
    putch(getch());
    putch(getch());
    putch(getch());
    putch(getch());
    putch(getch());
    uint8_t l_lsb = getch();
    putch(l_lsb);
    
    for(uint8_t i = 0; i < l_lsb; i++){
        putch(getch());
    }
    
    return 0;
}
