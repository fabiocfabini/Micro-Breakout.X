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
    MOVWF TRISA,1 ; 0=out, 1=in. RA0 is input.
    
    BANKSEL ANSELA
    MOVLW 0b00000000
    MOVWF ANSELA,1 ; 0=digital;1=in. RA0 to potenciometer.
    
    
    ;===============
    ;CONFIGURE PORTB
    ;===============
    BANKSEL LATB
    CLRF LATB,1 ; Set all LatchB bits to zero
    
    BANKSEL LATB
    MOVLW 0b11110001 
    MOVWF LATB,1 ; 0=out, 1=in. RB0, RB1, RB2 are input.
    
    BANKSEL ANSELB
    MOVLW 0b00000001
    MOVWF ANSELB,1 ; 0=digital;1=in. RB0, RB1, RB2 are analog.
    
    
    ;===============
    ;CONFIGURE PORTC
    ;===============
    BANKSEL LATA
    CLRF LATA,1 ; Set all LatchC bits to zero

    
    ;===============
    ;CONFIGURE PORTC
    ;===============
    BANKSEL LATC
    CLRF LATC,1 ; Set all LatchC bits to zero
    
    BANKSEL TRISC
    MOVLW 0b10000000 ; 0=out, 1=in. RC7 will connect to RX
    MOVWF TRISC
    
    BANKSEL ANSELC
    CLRF ANSELC,1 ;All digital pins
    
    BANKSEL RC4PPS
    MOVLW 0b00001001  ; Q: WHAT VALUE MUST WE GIVE TO RC4PPS TO PUT THE EUSART1 TX IN PIN RC4? HINT: look in the 17.2 section of the datasheet, table 17.2
    MOVWF RC4PPS   ;place the EUSART1 (TX/CK) in RC4  
    
    BANKSEL RX1PPS
    
    ; Same as 0x17
    MOVLW 0b00010111   ; Q: WHAT VALUE MUST WE GIVE TO RX1PPS TO PUT THE EUSART1 RX IN PIN RC7? HINT: look in the PPS chapter of the datasheet
    MOVWF RX1PPS  ;place the EUSART1 (RX) in RC7
    
    
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
    
    ; Q: WHAT VALUE SHOULD WE PUT IN SP1BRGL AND SP1BRG1H TO GET A BAUD RATE OF 9600 BPS FOR A CLOCK SPEED OF 32 MHZ? HINT: CHECK SECTION 28.2
    BANKSEL SP1BRGL
    MOVLW 0b1000100
    MOVWF SP1BRGL
    BANKSEL SP1BRGH
    MOVLW 0b00000000
    MOVWF SP1BRGH
    
    BANKSEL TX1STA
    movlw 0b00100100   ;8 data bits, TX enabled, ASYNC
    movwf TX1STA
    
    BANKSEL BAUD1CON
    MOVLW 0b00001000
    MOVWF BAUD1CON
    
    ; Q: HERE YOU MUST ENABLE THE USART AND THE RECEIVER WITH REGISTER RC1STA
    BANKSEL RC1STA
    BSF RC1STA, 7 // SPEN ENABLED
    // 8 bit mode
    // SREN - Single Recieve
    BSF RC1STA, 4 // Continuous Receive Enable bit
    // The rest is 0 but we dont know about bit 3 ADDEN
    //BSF RC1STA, 3 // The rest is 0 but we dont know about bit 3 ADDEN
    
    
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
    
    
    ;================
    ;CONFIGURE TIMER0
    ;================
    BANKSEL T0CON0
    CLRF T0CON0
    
    BANKSEL T0CON0
    MOVLW 0b01100011 // SET THE POSTSCALER
    MOVWF T0CON0
    
    BANKSEL T0CON1
    MOVLW 0b01101100  //Q: SET THE PRESCALER TO ~= 16000
    MOVWF T0CON1
    
   
    BANKSEL TMR0L
    CLRF TMR0L  ;clear the counter
    
    
    ;================= // MAY BE WRONG
    ;ENABLE INTERRUPTS
    ;=================
    BANKSEL PIR0
    BCF PIR0, 5 ;clear timer interrupt flag
    BANKSEL PIR1
    BCF PIR1,0  ;clear ADC interrupt flag
    BANKSEL PIR3 
    BCF PIR3,5 ;clear RX1 interrupt flag
    
    BANKSEL PIE0
    BSF PIE0, 5  ; Q: enable timer int
    BANKSEL PIE3
    BSF PIE3, 5 ; Q: enable RX1 int
    
    BANKSEL T0CON0
    BSF T0CON0,7   ;start timer 0
    BANKSEL ADCON0  
    BSF ADCON0,7   ;ENABLE ADC
    
    
    ; Q: HERE YOU MUST ENABLE PERIPHERAL INTERRUPTIONS AND GLOBAL INTERRUPTIONS
    BANKSEL INTCON
    BSF INTCON, 7 // ENABLE INTERRUPTS FOR ALL
    BSF INTCON, 6 // ENABLE PERIPHERALS FOR ALL  
    
    RETURN