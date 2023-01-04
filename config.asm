#include <xc.inc>
    
GLOBAL _config ;define the function to link it with the C definition

    
PSECT text0,local,class=CODE,reloc=2
    
CONFIG FEXTOSC=0b100 ;deactivate external oscillator (to allow write to RA7)
CONFIG CSWEN=0b1 ;allow editing NDIV and NOSC for CLK config
CONFIG WDTE=OFF ;required to avoid WDT restarting micro all the time

    
_config:
    
    ;===============
    ;CONFIGURE PORTA
    ;===============
    BANKSEL LATA
    CLRF LATA,1 ; Set all LatchA bits to zero
    
    BANKSEL TRISA
    MOVLW 0b00000000 
    MOVWF TRISA,1 ; Define RA[4,5,6,7] as output
    
    BANKSEL ANSELA
    MOVLW 0b00000000
    MOVWF ANSELA,1 ; Define RA[4,5,6,7] as digital
    
    
    ;===============
    ;CONFIGURE PORTB
    ;===============
    BANKSEL LATB
    CLRF LATB,1 ; Set all LatchB bits to zero
    
    BANKSEL LATB
    MOVLW 0b11110001 
    MOVWF LATB,1 ; Define RB[0,4,5,6,7] as input
    
    BANKSEL ANSELB
    MOVLW 0b00000001
    MOVWF ANSELB,1 ; Define RB[0] as analog and RB[4,5,6,7] as digital

    
    ;===============
    ;CONFIGURE PORTC
    ;===============
    BANKSEL LATC
    CLRF LATC,1 ; Set all LatchC bits to zero
    
    BANKSEL TRISC
    MOVLW 0b10000000 ; RC7 will connect to RX
    MOVWF TRISC
    
    BANKSEL ANSELC
    CLRF ANSELC,1 ;All digital pins
    
    BANKSEL RC4PPS
    MOVLW 0b00001001 ; Put the EUSART1 TX in pin RC4 
    MOVWF RC4PPS  
    
    BANKSEL RX1PPS
    MOVLW 0b00010111 ; place the EUSART1 (RX) in RC7
    MOVWF RX1PPS
    
    
    ;===============
    ;CONFIGURE CLOCK
    ;===============
    BANKSEL OSCCON1
    MOVLW 0b01100000  ;NOSC=0110 (internal high speed osc)
    MOVWF OSCCON1,1   ;NDIV=0000 (divider=1, clk divided by 1)
    
    BANKSEL OSCFRQ
    MOVLW 0b0000110 ; HFFRQ 0110 -> clk= 32 MHz
    MOVWF OSCFRQ,1
    
    BANKSEL OSCEN
    MOVLW 0b01000000 ;internal clock @freq=OSCFRQ ativo
    MOVWF OSCEN,1
    
    
    ;===============
    ;CONFIGURE USART
    ;===============
    ;BR=9600 @ CLK=32 MHz    
    
    BANKSEL SP1BRGL
    MOVLW 0b00011001 ; Make baudrate 19200 bits/sec
    MOVWF SP1BRGL
    BANKSEL SP1BRGH
    MOVLW 0b00000000
    MOVWF SP1BRGH
    
    BANKSEL TX1STA
    movlw 0b00100000   ;8 data bits, TX enabled, ASYNC
    movwf TX1STA
    
    BANKSEL RC1STA
    BSF RC1STA, 7 // SPEN ENABLED
    // 8 bit mode
    // SREN - Single Recieve
    BSF RC1STA, 4 // Continuous Receive Enable bit
    
    ;=============
    ;CONFIGURE ADC
    ;=============
    BANKSEL ADREF
    MOVLW 0b00000000  ;Vref set to vdd and vss
    MOVWF ADREF,1
    
    BANKSEL ADCLK // n = 15
    MOVLW 0b00000011   ; Q: SET THE ADC CLOCK FREQUENCY TO 1 MHZ, KNOWING THAT FOSC = 32 MHZ
    MOVWF ADCLK,1
    
    BANKSEL ADCON0
    MOVLW 0b00000000
    MOVWF ADCON0
    
    ;=================
    ;ENABLE INTERRUPTS
    ;=================
    BANKSEL PIR0
    BCF PIR0, 5 ;clear timer interrupt flag
    BANKSEL PIR1
    BCF PIR1,0  ;clear ADC interrupt flag
    BANKSEL PIR3 
    BCF PIR3,5 ;clear RX1 interrupt flag
    
    BANKSEL PIE3
    BSF PIE3, 5 ; Q: enable RX1 int
    
    BANKSEL ADCON0  
    BSF ADCON0,7   ;ENABLE ADC
    
    BANKSEL INTCON
    BSF INTCON, 7 // ENABLE INTERRUPTS FOR ALL
    BSF INTCON, 6 // ENABLE PERIPHERALS FOR ALL  
    
    RETURN