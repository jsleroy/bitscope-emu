#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Emulate BitScope VM 112
#
# See:
# http://www.bitscope.com/pic/
#-------------------------------------------------------------------------------


import serial
import time

eeprom = {}

def reset(cmd):
    """Reset the Virtual Machine. Print the Byte-Code number."""
    for idx in range(len(registers)):
        registers[idx] = 0
    #s.write(cmd)

def version(cmd):
    """Print the 8 character string identifying the revision."""
    s.write(cmd)
    s.write('\r')
    for c in "BC000100":
        s.write(c)
    s.write('\r')

def clear(cmd):
    """Clear R0. Usually commences byte entry."""
    registers[0] = 0
    print " " * 17,
    print "RO {0:#04x} {1}".format(registers[0], BitScope.registers[0])
    s.write(cmd)

def swap(cmd):
    """Swap nibbles in R0. Usually concludes byte entry."""
    h = (registers[0] & 0x0F) << 4
    l = (registers[0] & 0xF0) >> 4
    registers[0] = l | h
    print " " * 17,
    print "RO {0:#04x} {1}".format(registers[0], BitScope.registers[0])
    s.write(cmd)

def input(cmd):
    """Increment R0 and nibble swap."""
    if cmd in "0123456789":
        value = ord(cmd) - ord('0')
    elif cmd in "abcdef":
        value = ord(cmd) - ord('a') + 10
    else:
        raise Exception
    registers[0] += value
    h = (registers[0] & 0x0F) << 4
    l = (registers[0] & 0xF0) >> 4
    registers[0] = l | h
    print " " * 17,
    print "RO {0:#04x} {1}".format(registers[0], BitScope.registers[0])
    s.write(cmd)

def mov(cmd, src, dst):
    registers[dst] = registers[src]
    print " " * 17,
    print "R{0} {1:#04x} {2}".format(dst, registers[dst], BitScope.registers[dst])

def copy1(cmd):
    """Copy R0 to Address Register R1."""
    mov(cmd, 0, 1)
    s.write(cmd)

def copy2(cmd):
    """Copy R0 to Address Register R2."""
    mov(cmd, 0, 2)
    s.write(cmd)

def store(cmd):
    """Store. Copy R0 to register (R1)."""
    mov(cmd, 0, registers[1])
    s.write(cmd)

def load(cmd):
    """Load. Copy register (R2) to R0."""
    mov(cmd, registers[2], 0)
    s.write(cmd)

def add(cmd, dst, value):
    registers[dst] += value
    print " " * 17,
    print "R{0} {1:#04x} {2}".format(dst, registers[dst], BitScope.registers[dst])

def incr1(cmd):
    """Increment Address Register R1."""
    add(cmd, 1, 1)
    s.write(cmd)

def incr(cmd):
    """Increment Register (R1)."""
    add(cmd, registers[1], 1)
    s.write(cmd)

def decr(cmd):
    """Decrement Register (R1)."""
    add(cmd, registers[1], -1)
    s.write(cmd)

def display(cmd):
    """Print register (R1)."""
    s.write(cmd)
    s.write('\r')
    s.write(chr(registers[1] >> 4))
    s.write(chr(registers[1] & 0xF))
    s.write('\r')

def spoke_write(cmd):
    """Program Spock Registers from R3...R7."""
    s.write(cmd)

def spoke_read(cmd):
    """Capture Spock Counter to R9,R10."""
    s.write(cmd)

def pod_read(cmd):
    """Transmit byte in R18 to POD IO-0."""
    s.write(cmd)

def eeprom_read(cmd):
    """Read EEPROM byte at address (R17) and print."""
    value = eeprom.get(registers[17], 0x00)
    s.write(cmd)
    s.write('\r')
    s.write(chr(value >> 4))
    s.write(chr(value & 0xF))
    s.write('\r')

def eeprom_write(cmd):
    """Write byte R16 to EEPROM address (R17)."""
    eeprom[registers[17]] = registers[16]
    s.write(cmd)

class BitScope:
    bytecode = {
        '\x00': reset,
        '\x21': reset,
        '?': version,
        '[': clear,
        '0': input,
        '1': input,
        '2': input,
        '3': input,
        '4': input,
        '5': input,
        '6': input,
        '7': input,
        '8': input,
        '9': input,
        'a': input,
        'b': input,
        'c': input,
        'd': input,
        'e': input,
        'f': input,
        ']': swap,
        '@': copy1,
        '#': copy2,
        's': store,
        'l': load,
        'p': display,
        'n': incr1,
        '+': incr,
        '-': decr,
        '>': spoke_write,
        '<': spoke_read,
        "|": pod_read,
        "r": eeprom_read,
        "w": eeprom_write,
    }

    registers = (
        "Data Register",
        "Address Register",
        "Source Address Register",
        "Sample Pre-load (Low Byte)",
        "Sample Pre-load (High Byte)",
        "Trigger Logic Byte",
        "Trigger Mask Byte",
        "Spock Option Byte",
        "Trace Register",
        "Counter Capture (Low Byte)",
        "Counter Capture (High Byte)",
        "Post Trigger Delay (Low Byte)",
        "Post Trigger Delay (High Byte)",
        "Time-base Expansion",
        "Input/Attenuation",
        "Dump Size",
        "EEPROM Data",
        "EEPROM Address",
        "POD Transmit",
        "POD Receive",
        "Pre-Trigger Delay",
        "Frequency Timer Pre-Load",
        "Frequency Pre-scale",
        "Period Pulse Count",
    )

registers = [0] * len(BitScope.registers)


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--device', type=str)
args = parser.parse_args()

s = serial.Serial(args.device)

pc = 0

while True:
    # Receive command
    cmd = s.read(1)

    # Execute command
    try:
        f = BitScope.bytecode[cmd]
        doc = f.__doc__
    except KeyError:
        f = None
        doc = "???"
    print "{0:>8d} {1} ({2:#04x}) {3}".format(pc, cmd, ord(cmd), doc)

    if f is not None:
        f(cmd)

    # Increment program counter
    pc += 1
