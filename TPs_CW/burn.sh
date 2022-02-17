#!/usr/bin/env nix-shell
#!nix-shell default.nix -i python3

import chipwhisperer as cw
scope = cw.scope()

prog = cw.programmers.XMEGAProgrammer
cw.program_target(scope, prog, "myappTP/aes.hex")
