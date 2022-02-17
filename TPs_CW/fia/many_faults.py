'''
File: many_faults.py
Created Date: Friday December 17th 2021
Author: Ronan (ronan.lashermes@inria.fr)
-----
Last Modified: Tuesday, 1st February 2022 3:06:46 pm
Modified By: Ronan (ronan.lashermes@inria.fr>)
-----
Copyright (c) 2021
'''

import chipwhisperer as cw
from chipwhisperer.common.utils.aes_cipher import AESCipher
from chipwhisperer.analyzer.utils.aes_funcs import key_schedule_rounds
import chipwhisperer.common.results.glitch as glitch
from tqdm import tqdm
import time
import numpy as np

def reboot_flush(scope, target, key, target_round):
        scope.io.pdic = False
        time.sleep(0.1)
        scope.io.pdic = "high_z"
        time.sleep(0.1)
        #Flush garbage too
        target.flush()
        time.sleep(0.5)
        target.set_key(key)
        target.simpleserial_write('t', bytearray([target_round]))
        target.simpleserial_wait_ack()
        print("reboot")

def aes_verif(pt, key):
    exp_key = list(key)
    rounds = 10
    #expand key
    for i in range(1, rounds+1):
        exp_key.extend(key_schedule_rounds(list(key), 0, i))

    cipher = AESCipher(exp_key)
    return bytearray(cipher.cipher_block(list(pt)))

# connect to chipwhisperer
scope = cw.scope()
# setup scope with default parameters
scope.default_setup()
# scope.glitch.clk_src = "clkgen"
# scope.glitch.width = 10.0 #[-49.8, 49.8]
# scope.glitch.width_fine = 0 #[-255,255]
# scope.glitch.offset = -3.0 #[-49.8,49.8]
# scope.glitch.offset_fine = 0 #[-255,255]
# scope.glitch.trigger_src = "ext_single"

# scope.glitch.repeat = 10
# scope.glitch.output = "clock_xor"
# scope.io.hs2 = "glitch"

scope.glitch.clk_src = "clkgen" # set glitch input clock
scope.glitch.output = "clock_xor" # glitch_out = clk ^ glitch
scope.glitch.trigger_src = "ext_single" # glitch only after scope.arm() called
scope.glitch.repeat = 1
scope.io.hs2 = "glitch"  # output glitch_out on the clock line

scope.glitch.width = 7.0
scope.glitch.offset = -2.0
scope.glitch.ext_offset = 4
target_round = 10

# target = microcontroller
target = cw.target(scope)


ktp = cw.ktp.Basic()
key, pt = ktp.new_pair()

# key = bytearray([0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c])
# pt = bytearray([0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34])
reboot_flush(scope, target, key, target_round)
diff0 = [0 for _ in range(16)]

repetition = 1000
fcts = []
cts = []
faults_count = 0

for i in tqdm(range(repetition)):
    pt = ktp.next_text()
    if scope.adc.state:
        # can detect crash here (fast) before timing out (slow)
        # print("Trigger still high!")
        #Device is slow to boot?
        reboot_flush(scope, target, key, target_round)

    scope.arm()
    ct_verif = aes_verif(pt, key)
    target.simpleserial_write('p', pt)
    val = target.simpleserial_read_witherrors('r', len(ct_verif), glitch_timeout = 10)
    valid = val['valid']
    if valid:
        ct = val['payload']
        if ct is None:
            continue
        else:
            diff = [ct_verif[j] ^ ct[j] for j in range(len(ct))]
            if diff != diff0:
                fcts.append(ct)
                cts.append(ct_verif)
                faults_count += 1
                
    else:
        reboot_flush(scope, target, key, target_round)

npcts = np.asarray(cts)
npfcts = np.asarray(fcts)

np.save("cts.npy", npcts)
np.save("fcts.npy", npfcts)

print(str(faults_count) + " faults have been injected.")
print("The End")