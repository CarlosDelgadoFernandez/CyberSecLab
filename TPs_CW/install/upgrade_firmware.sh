#!/usr/bin/env nix-shell
#!nix-shell ../default.nix -i python3

print("*******")
print("If you are stuck in boot mode (red and blue LEDs blinking faste) after executing this script: kill it then call 'recover_bricked_cw'.")
print("*******")

import chipwhisperer as cw

# Connect to scope
scope = cw.scope()

programmer = cw.SAMFWLoader(scope=scope)
programmer.auto_program()


