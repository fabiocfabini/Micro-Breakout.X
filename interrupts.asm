#include <xc.inc>

    
GLOBAL _int_handler, _adc_result, _interpret_ncap_cmd, _read_ncap_cmd, _echo_rec_bytes, _echo_single_byte    ;declare global functions
    
PSECT intcode

#define parcel_msb 0


_int_handler:    ;when an interrupt happens, this function is called. It is your job to verify what interrupt happened and act accordingly
    BANKSEL PIR0
    BTFSC PIR0, 5 ; Q:check if the timer0 interrupt flag is set. If so, go to timer0_int_handler. If not, skip.
    goto _timer0_int_handler
    
    BANKSEL PIR3
    BTFSC PIR3, 5   ;Q: check if the EUSART1 RX flag is set. If so, go to the C function _getch. If not, skip.  
    call _interpret_ncap_cmd
    
    RETFIE
    
    

_timer0_int_handler:
    //BANKSEL ADCON0
    //BSF ADCON0, 0, 1 ;Q: WE CAN USE THE TIMER TO CONTROL THE ADC SAMPLING RATE! START AN ADC CONVERSION HERE
    BANKSEL PORTA
    BTG PORTA,4  ;TOGGLE LED ON PORTA,5
    BANKSEL PIR0
    BCF PIR0,5 ;clear timer_int flag
    RETFIE  ;return from interruption
