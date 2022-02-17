#!/usr/bin/env nix-shell
#!nix-shell ../default.nix -i python3

import chipwhisperer as cw


programmer = cw.SAMFWLoader(scope=None)
programmer.program('/dev/ttyACM0', hardware_type='cwlite')


