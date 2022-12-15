#ifndef TEDS_H
#define	TEDS_H

/******************************************************
* TRANSDUCER ELECTRONIC DATA SHEET TEMPLATE INTERFACE *
*******************************************************/
#include <xc.h>
#include <stdint.h>

// TEDS IDs
#define META_TEDS_ID 1
#define TRANSDUCER_TEDS_ID 3

typedef uint8_t TLV;

#define META_ID_L       (2 +  4)    // [0]: type; [1]: length; [2:5]: Value(FAMILY, CLASS, VERSION, TUPLE LENGHT)  
#define META_UUID_L     (2 + 10)    // [0]: type; [1]: length; [2:11]: Value(UUID)
#define META_MAXCHAN_L  (2 +  2)    // [0]: type; [1]: length; [2:3]: Value(MAXCHAN)

typedef struct {
    TLV id[META_ID_L];                  // What type of TEDS is this?               | ALWAYS THE SAME
    TLV uuid[META_UUID_L];              // What is the UUID of this TEDS?           | HAS TO BE UNIQUE
    TLV max_channels[META_MAXCHAN_L];   // How many channels does this TEDS have?   ? HOW MANY CHANNELS
} META_TEDS;

/*
 * @brief This function defines the META TEDS Information at a global level
*/
void init_meta_teds(void);

/*
 * @brief This function sends the META TEDS Information through the UART interface.
*/
void send_meta_teds(void);

// DATA BLOCKS FOT TCT's

#define TCT_ID_L                (2 +  4)    // [0]: type; [1]: length;  [2:5]:  Value(FAMILY, CLASS, VERSION, TUPLE LENGHT)
#define TCT_TYPE_L              (2 +  1)    // [0]: type; [1]: length;    [2]:  Value(TYPE)
#define TCT_UNIT_L              (2 + 10)    // [0]: type; [1]: length; [2:11]:  Value(UNIT)
#define TCT_LOW_RANGE_LIMIT_L   (2 +  1)    // [0]: type; [1]: length;    [2]:  Value(LOW RANGE LIMIT)
#define TCT_HIGH_RANGE_LIMIT_L  (2 +  1)    // [0]: type; [1]: length;    [2]:  Value(HIGH RANGE LIMIT)
#define TCT_DATA_MODEL_L        (2 +  1)    // [0]: type; [1]: length;    [2]:  Value(DATA MODEL)
#define TCT_DATA_LENGTH_L       (2 +  1)    // [0]: type; [1]: length;    [2]:  Value(DATA LENGTH)
#define TCT_DATA_SB_L           (2 +  1)    // [0]: type; [1]: length;    [2]:  Value(DATA SB)

typedef struct {
    TLV id[TCT_ID_L];                               // What type of TEDS is this?                       | ALWAYS THE SAME
    TLV type[TCT_TYPE_L];                           // What is the type of this TCT?                    | SENSOR or ACTUATOR
    TLV units[TCT_UNIT_L];                          // What are the units of this TCT?                  ? WHAT UNITS
    TLV low_range_limit[TCT_LOW_RANGE_LIMIT_L];     // What is the low range limit of this TCT?         ? LOW VALUE
    TLV high_range_limit[TCT_HIGH_RANGE_LIMIT_L];   // What is the high range limit of this TCT?        ? HIGH VALUE
    TLV data_model[TCT_DATA_MODEL_L];               // What is the data type of this TCT?               | Always 0
    TLV data_model_length[TCT_DATA_LENGTH_L];       // What is the data length of this TCT?             | Always 1    
    TLV data_model_sb[TCT_DATA_SB_L];               // How many significant bits does this TCT have?    | Always 8    
} TC_TEDS;

/*
 * @brief This function defines the TC TEDS Information at a global level
*/
void init_tc_teds(void);

/*
 * @brief This function sends the META TEDS Information through the UART interface.
 * @param channel Which transducer channel to send.
*/
void send_tc_teds(uint8_t channel);

/*
 * @brief This function sends any TLV data through the UART interface.
*/
void send_TLV(TLV *tlv);

/*****************
* IMPLEMENTATION *
******************/
#ifdef TEDS_IMPLEMENTATION
#include <string.h>

static META_TEDS meta_teds;

#define NUM_TCT 5
static TC_TEDS tcts[NUM_TCT];

void init_meta_teds(){
    // Copy the META TEDS Information
    TLV id_info[META_ID_L] = {3, 4, 0, 1, 0, 1};
    memcpy(meta_teds.id, id_info, META_ID_L);

    // Copy the UUID
    TLV uuid_info[META_UUID_L] = {4, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1};
    memcpy(meta_teds.uuid, uuid_info, META_UUID_L);

    // Copy the MAX CHANNELS
    TLV max_channels_info[META_MAXCHAN_L] = {13, 2, 0, 3};
    memcpy(meta_teds.max_channels, max_channels_info, META_MAXCHAN_L);
}

void init_tc_teds(){
    /* Channel 0 - Accelerometer X - Sensor */
    #define CHAN_ACC_X 0
    TLV id_info[TCT_ID_L] = {3, 4, 0, 3, 0, 1};
    memcpy(tcts[0].id, id_info, TCT_ID_L);

    TLV type_info[TCT_TYPE_L] = {11, 1, 0};
    memcpy(tcts[0].type, type_info, TCT_TYPE_L);
    //                                       rad  strad  m    Kg   s    A    K    n    can
    TLV units_info[TCT_UNIT_L] = {12, 10, 0, 128,   128, 130, 128, 124, 128, 128, 128, 128};
    memcpy(tcts[0].units, units_info, TCT_UNIT_L); //TODO: Does it measure m/s^2? Or Volts?

    TLV low_range_limit_info[TCT_LOW_RANGE_LIMIT_L] = {13, 1, 0};
    memcpy(tcts[0].low_range_limit, low_range_limit_info, TCT_LOW_RANGE_LIMIT_L);

    TLV high_range_limit_info[TCT_HIGH_RANGE_LIMIT_L] = {14, 1, 255};
    memcpy(tcts[0].high_range_limit, high_range_limit_info, TCT_HIGH_RANGE_LIMIT_L);

    TLV data_model_info[TCT_DATA_MODEL_L] = {40, 1, 0};
    memcpy(tcts[0].data_model, data_model_info, TCT_DATA_MODEL_L);

    TLV data_model_length_info[TCT_DATA_LENGTH_L] = {41, 1, 1};
    memcpy(tcts[0].data_model_length, data_model_length_info, TCT_DATA_LENGTH_L);

    TLV data_model_sb_info[TCT_DATA_SB_L] = {42, 1, 8};
    memcpy(tcts[0].data_model_sb, data_model_sb_info, TCT_DATA_SB_L);

    /* Channel 1 - Accelerometer Y - Sensor*/
    #define CHAN_ACC_Y 1
    memcpy(tcts[1].id, id_info, TCT_ID_L);
    
    memcpy(tcts[1].type, type_info, TCT_TYPE_L);
    
    memcpy(tcts[1].units, units_info, TCT_UNIT_L); //TODO: Does it measure m/s^2? Or Volts?

    memcpy(tcts[1].low_range_limit, low_range_limit_info, TCT_LOW_RANGE_LIMIT_L);

    memcpy(tcts[1].high_range_limit, high_range_limit_info, TCT_HIGH_RANGE_LIMIT_L);

    memcpy(tcts[1].data_model, data_model_info, TCT_DATA_MODEL_L);

    memcpy(tcts[1].data_model_length, data_model_length_info, TCT_DATA_LENGTH_L);

    memcpy(tcts[1].data_model_sb, data_model_sb_info, TCT_DATA_SB_L);

    /* Channel 2 - Potentiometer - Sensor */
    #define CHAN_POTEN 2
    memcpy(tcts[2].id, id_info, TCT_ID_L);

    memcpy(tcts[2].type, type_info, TCT_TYPE_L);
    //                                       rad  strad  m    Kg   s    A    K    n    can
    TLV units_info_2[TCT_UNIT_L] = {12, 10, 0, 128,   128, 132, 130, 122, 126, 128, 128, 128};
    memcpy(tcts[2].units, units_info_2, TCT_UNIT_L); //TODO: Does it measure m/s^2? Or Volts?

    memcpy(tcts[2].low_range_limit, low_range_limit_info, TCT_LOW_RANGE_LIMIT_L);

    memcpy(tcts[2].high_range_limit, high_range_limit_info, TCT_HIGH_RANGE_LIMIT_L);

    memcpy(tcts[2].data_model, data_model_info, TCT_DATA_MODEL_L);

    memcpy(tcts[2].data_model_length, data_model_length_info, TCT_DATA_LENGTH_L);

    memcpy(tcts[2].data_model_sb, data_model_sb_info, TCT_DATA_SB_L);
    
    /* Channel 3 - Led on Pin RA6 - Actuator */
    #define CHAN_LED_RA6 3
    memcpy(tcts[3].id, id_info, TCT_ID_L);
    
    TLV type_info_3[TCT_TYPE_L] = {11, 1, 1};
    memcpy(tcts[3].type, type_info_3, TCT_TYPE_L);

    memcpy(tcts[3].units, units_info_2, TCT_UNIT_L); //TODO: Does it measure m/s^2? Or Volts?

    memcpy(tcts[3].low_range_limit, low_range_limit_info, TCT_LOW_RANGE_LIMIT_L);

    memcpy(tcts[3].high_range_limit, high_range_limit_info, TCT_HIGH_RANGE_LIMIT_L);

    memcpy(tcts[3].data_model, data_model_info, TCT_DATA_MODEL_L);

    memcpy(tcts[3].data_model_length, data_model_length_info, TCT_DATA_LENGTH_L);

    memcpy(tcts[3].data_model_sb, data_model_sb_info, TCT_DATA_SB_L);
    
    /* Channel 4 - Led on Pin RA7 - Actuator */
    #define CHAN_LED_RA7 4
    memcpy(tcts[4].id, id_info, TCT_ID_L);

    memcpy(tcts[4].type, type_info_3, TCT_TYPE_L);

    memcpy(tcts[4].units, units_info_2, TCT_UNIT_L); //TODO: Does it measure m/s^2? Or Volts?

    memcpy(tcts[4].low_range_limit, low_range_limit_info, TCT_LOW_RANGE_LIMIT_L);

    memcpy(tcts[4].high_range_limit, high_range_limit_info, TCT_HIGH_RANGE_LIMIT_L);

    memcpy(tcts[4].data_model, data_model_info, TCT_DATA_MODEL_L);

    memcpy(tcts[4].data_model_length, data_model_length_info, TCT_DATA_LENGTH_L);

    memcpy(tcts[4].data_model_sb, data_model_sb_info, TCT_DATA_SB_L);
}

#ifdef TEDS_DEBUG

void send_meta_teds();
void send_tc_teds(uint8_t channel);
void send_TLV(TLV *tlv);

void send_meta_teds(){
    printf("META TEDS:\n");
    printf("\tid:\n");
    send_TLV(meta_teds.id);
    printf("\tuuid:\n");
    send_TLV(meta_teds.uuid);
    printf("\tmax channel:\n");
    send_TLV(meta_teds.max_channels);
};

void send_tc_teds(uint8_t channel){
    printf("TC TEDS %d:\n", channel);
    printf("\tid:\n");
    send_TLV(tcts[channel].id);
    printf("\ttype:\n");
    send_TLV(tcts[channel].type);
    printf("\tunits:\n");
    send_TLV(tcts[channel].units);
    printf("\tlow range:\n");
    send_TLV(tcts[channel].low_range_limit);
    printf("\thigh range:\n");
    send_TLV(tcts[channel].high_range_limit);
    printf("\tdata model:\n");
    send_TLV(tcts[channel].data_model);
    printf("\tdata model length:\n");
    send_TLV(tcts[channel].data_model_length);
    printf("\tdata SB:\n");
    send_TLV(tcts[channel].data_model_sb);
}

void send_TLV(TLV *tlv){;
    printf("\t\tType: ");
    printf("%d", tlv[0]);
    printf("\n");

    printf("\t\tLength: ");
    printf("%d", tlv[1]);
    printf("\n");

    printf("\t\tValue: ");
    for(int i = 0; i < tlv[1]; i++){
        printf("%d ", tlv[2+i]);
    }
    printf("\n");
}

#else

void send_meta_teds(){
    putch(1);                                           // Exit code
    putch(0);                                           // MSB of returned data length
    putch(META_ID_L + META_UUID_L + META_MAXCHAN_L);    // LSB of returned data length
    
    send_TLV(meta_teds.id);
    send_TLV(meta_teds.uuid);
    send_TLV(meta_teds.max_channels);
};

void send_tc_teds(uint8_t channel){
    putch(1);                                               // Exit code
    putch(0);                                               // MSB of returned data length
    putch(TCT_ID_L + TCT_TYPE_L + TCT_UNIT_L + TCT_LOW_RANGE_LIMIT_L + TCT_HIGH_RANGE_LIMIT_L + TCT_DATA_MODEL_L + TCT_DATA_LENGTH_L + TCT_DATA_SB_L);  // LSB of returned data length

    send_TLV(tcts[channel].id);
    send_TLV(tcts[channel].type);
    send_TLV(tcts[channel].units);
    send_TLV(tcts[channel].low_range_limit);
    send_TLV(tcts[channel].high_range_limit);
    send_TLV(tcts[channel].data_model);
    send_TLV(tcts[channel].data_model_length);
    send_TLV(tcts[channel].data_model_sb);
}

void send_TLV(TLV *tlv){
    putch(tlv[0]);
    putch(tlv[1]);
    for(int i = 0; i < tlv[1]; i++){
        putch(tlv[2+i]);
    }
};

#endif // __XC8

#endif // TEDS_IMPLEMENTATION

#endif	// TEDS_H