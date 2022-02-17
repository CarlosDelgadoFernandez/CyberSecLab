'''
File: trace2000.py
Created Date: Monday December 20th 2021
Author: Ronan (ronan.lashermes@inria.fr)
-----
Last Modified: Monday December 20th 2021
Modified By: Ronan (ronan.lashermes@inria.fr>)
-----
Copyright (c) 2021
'''

import chipwhisperer as cw
import numpy as np
from tqdm import tqdm

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
target.simpleserial_write('t', bytearray([1]))
target.simpleserial_wait_ack()

ktp = cw.ktp.Basic()
key, pt = ktp.next()
target.set_key(key)
traces = []
pts = []
cts = []

# tqdm is there to show a progress bar
for i in tqdm(range(2000)):
    pt = ktp.next_text()
    trace = cw.capture_trace(scope, target, pt, key)
    traces.append(trace.wave)
    pts.append(trace.textin)
    cts.append(trace.textout)

nptraces = np.asarray(traces)
np.save("traces.npy", nptraces)

nppts = np.asarray(pts)
np.save("pts.npy", nppts)

npcts = np.asarray(cts)
np.save("cts.npy", npcts)
