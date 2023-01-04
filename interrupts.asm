#include <xc.inc>

    
GLOBAL _int_handler, _interpret_ncap_cmd, _read_ncap_cmd, _echo_rec_bytes, _echo_single_byte ;declare global functions
    
PSECT intcode

_int_handler:
    BANKSEL PIR3
    BTFSC PIR3, 5   ;check if the EUSART1 RX flag is set. If so, go to the C interpret_ncap_cmd. If not, skip.  
    call _interpret_ncap_cmd
    
    RETFIE
