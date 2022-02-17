/**
* @Author: hélène, ronan
* @Date:   12-09-2016
* @Email:  helene.le-bouder@imt-atlantique.fr, ronan.lashermes@inria.fr
* @Last modified by:   helene
* @Last modified time: 08-10-2018
* @License: GPL
*/

#include "aes.h"
#include "hal/hal.h"
#include "hal/simpleserial.h"
#include <stdint.h>
#include <stdlib.h>

uint8_t plaintext[DATA_SIZE];
uint8_t ciphertext[DATA_SIZE];
uint8_t key[DATA_SIZE];
uint8_t targeted_round = 1;



uint8_t set_key(uint8_t* k, uint8_t len)
{
    if (len != DATA_SIZE) {
        led_error(1);
        return 0x01;
    }

	for(int i = 0; i < DATA_SIZE; i++) {
        key[i] = k[i];
    }
    led_error(1);
	return 0x00;
}

uint8_t set_round(uint8_t* r, uint8_t len) {
    if (len != 1) {
        led_error(1);
        return 0x01;
    }
    targeted_round = r[0];
    return 0x00;
}
uint8_t set_pt(uint8_t* pt, uint8_t len)
{
    if (len != DATA_SIZE) {
        led_error(1);
        return 0x01;
    }

    for(int i = 0; i < DATA_SIZE; i++) {
        plaintext[i] = pt[i];
    }
	//trigger_high();

    /*
    Encrypt here using ciphertext, plaintext and key variables.
    */
	AESEncrypt(ciphertext, plaintext,key);
	
	//trigger_low();
	simpleserial_put('r', 16, ciphertext);//send response
	return 0x00;
}

uint8_t reset(uint8_t* x, uint8_t len)
{
    // Reset key here if needed
	return 0x00;
}


int main(void)
{
    platform_init();
    init_uart();
    trigger_setup();

    led_ok(1);
    led_error(0);

    simpleserial_init();
    simpleserial_addcmd('k', 16, set_key);
    simpleserial_addcmd('p', 16,  set_pt);
    simpleserial_addcmd('x',  0,   reset);
    simpleserial_addcmd('t', 1, set_round);


    while(1) {
        simpleserial_get();// get next command and react to it
    }
}
