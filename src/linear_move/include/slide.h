#include <errno.h>
#include <unistd.h>
#include <string.h>
#include <boost/thread.hpp>
#include <math.h>
#include "modbus/modbus.h"

#define SLAVE_ID 0x7F
#define Pos_Address 0x520
#define Servo_on_Adress 0x23C
#define path1_def_Address 0x604
#define path1_data_Address 0x606
#define move_Address 0x50E
#define jog_Adress 0x40A
#define check_pos_Address 0x05C
#define Registers_Lenth 2

uint16_t servo_on[2] = {0001,0000};
uint16_t servo_off[2] = {0000,0000};
uint16_t path_def[2] = {0x0002,0x0005};

uint16_t path_data[2] = {0x0000,0x0000};

uint16_t move_point[2] = {0x0001,0x0000};

uint16_t jog_data[2] = {2000,0000};
uint16_t dest[2];

modbus_t *ctx=nullptr;
