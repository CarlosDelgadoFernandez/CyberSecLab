'''
File: delay.py
Created Date: Friday December 17th 2021
Author: Ronan (ronan.lashermes@inria.fr)
-----
Last Modified: Tuesday, 1st February 2022 2:59:17 pm
Modified By: Ronan (ronan.lashermes@inria.fr>)
-----
Copyright (c) 2021
'''

import chipwhisperer as cw
from chipwhisperer.common.utils.aes_cipher import AESCipher
from chipwhisperer.analyzer.utils.aes_funcs import key_schedule_rounds
import chipwhisperer.common.results.glitch as glitch
import matplotlib.pylab as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
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
# scope.glitch.ext_offset = 100
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
target_round = 10

# target = microcontroller
target = cw.target(scope)

ktp = cw.ktp.Basic()
key, pt = ktp.new_pair()
# key = bytearray([0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c])
# pt = bytearray([0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34])
# target.set_key(key)
reboot_flush(scope, target, key, target_round)
diff0 = bytearray([0 for _ in range(16)])

repetition = 1
delay_range = range(0, 100)

fault_grid = np.zeros(len(delay_range))
crash_grid = np.zeros(len(delay_range))
ind_width = 0
# print(len(fault_grid))
print("Exploring parameter ext_offset")

for d in delay_range:
    scope.glitch.ext_offset = d
    
        # print("Width: " + str(lwidth) + " | Offset: " + str(loff))

    for i in range(repetition):
        # pt = ktp.next_text()
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
                crash_grid[d] += 1
                # print("Width: " + str(lwidth) + " | Offset: " + str(loff))
                continue
            else:
                diff = bytearray([ct_verif[j] ^ ct[j] for j in range(len(ct))])
                # print(diff)
                if diff != diff0:
                    fault_grid[d] += 1
                    print(diff.hex() + " at " + str(d))
                else:
                    print("No fault at " + str(d))
        else:
            # print("Width: " + str(lwidth) + " | Offset: " + str(loff))
            crash_grid[d] += 1
            reboot_flush(scope, target, key, target_round)


plt.show()