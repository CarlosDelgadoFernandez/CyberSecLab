'''
File: trace1.py
Project: 12correction-NUEVA
Created Date: Friday December 17th 2021
Author: Ronan (ronan.lashermes@inria.fr)
-----
Last Modified: Friday December 17th 2021
Modified By: Ronan (ronan.lashermes@inria.fr>)
-----
Copyright (c) 2021
'''

import chipwhisperer as cw
import matplotlib.pyplot as plt

# connect to chipwhisperer
scope = cw.scope()
# setup scope with default parameters
# Sets up sane capture defaults for this scope
#         25dB gain
#         5000 capture samples
#         0 sample offset
#         rising edge trigger
#         7.37MHz clock output on hs2
#         4*7.37MHz ADC clock
#         tio1 = serial rx
#         tio2 = serial tx
#         CDC settings change off


scope.default_setup()
scope.adc.samples = 1000


# target = microcontroller
target = cw.target(scope)

ktp = cw.ktp.Basic()
key, pt = ktp.new_pair()

target.set_key(key)

target.simpleserial_write('t', bytearray([1]))
target.simpleserial_wait_ack()

trace = cw.capture_trace(scope, target, pt, key)
plt.plot(trace.wave)
plt.show()

