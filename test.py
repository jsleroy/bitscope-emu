# import serial
# ser = serial.Serial('/dev/ttyS0')  # open first serial port
# print ser.name          # check which port was really used
# ser.write("hello")      # write a string
# ser.close()             # close port


import os, pty, serial
import serial

class BitScope:
    versions = (
      "BS000500", # 0
      "BS000501", # 1
      "BS001001", # 2
      "BS001002", # 3
      "BS001003", # 4
      "BS001004", # 5
      "BS005000", # 6
      "BS010000", # 7
      "BS012000", # 8
      "BS031000", # 9
      "BS031100", # 10
      "BS032000", # 11
      "BS032500", # 12
      "BS032600", # 13
      "BS044200", # 14
      "BS044201", # 15
      "BS044202", # 16
      "BS044500", # 17
      "BS044501", # 18
    )

    bytecode = {
        0x00: ("Reset the Virtual Machine. Print the Byte-Code number.", reset),
        0x21: ("Soft VM reset.", reset),
        0x23: ("Set Source Address Register R2.", None),
        0x2B: ("Increment register (R1).", None),
        0x30: ("Increment R0 by 0 and nibble swap.", reg_update),
        0x31: ("Increment R0 by 1 and nibble swap.", reg_update),
        0x32: ("Increment R0 by 2 and nibble swap.", reg_update),
        0x33: ("Increment R0 by 3 and nibble swap.", reg_update),
        0x34: ("Increment R0 by 4 and nibble swap.", reg_update),
        0x35: ("Increment R0 by 5 and nibble swap.", reg_update),
        0x36: ("Increment R0 by 6 and nibble swap.", reg_update),
        0x37: ("Increment R0 by 7 and nibble swap.", reg_update),
        0x38: ("Increment R0 by 8 and nibble swap.", reg_update),
        0x39: ("Increment R0 by 9 and nibble swap.", reg_update),
        0x3C: ("Capture Spock Counter to R9,R10.", None),
        0x3E: ("Program Spock Registers from R3...R7.", None),
        0x3F: ("Print the 8 character string identifying the revision.", None),
        0x40: ("Set Address Register R1.", None),
        0x41: ("Analog memory dump (Binary format, analogue data).", None),
        0x44: ("Delay until trigger and Trace, then print Spock Counter.", None),
        0x45: ("Scan for Event, then print Spock Counter.", None),
        0x4C: ("Trace Logic until trigger, then print Spock Counter.", None),
        0x4D: ("Mixed memory dump (Binary format, analogue & digital data).", None),
        0x50: ("Measure time Period.", None),
        0x52: ("Read EEPROM byte at address (R17) and print.", None),
        0x53: ("Sample dump (CSV format, analogue & digital data).", None),
        0x54: ("Trace until trigger + delay, then print Spock Counter.", None),
        0x55: ("Configure device hardware.", None),
        0x57: ("Write byte R16 to EEPROM address (R17).", None),
        0x5B: ("Clear R0. Usually commences byte entry.", None),
        0x5D: ("Swap nibbles in R0. Usually concludes byte entry.", None),
        0x61: ("Increment R0 by 10 and nibble swap.", reg_update),
        0x62: ("Increment R0 by 11 and nibble swap.", reg_update),
        0x63: ("Increment R0 by 12 and nibble swap.", reg_update),
        0x64: ("Increment R0 by 13 and nibble swap.", reg_update),
        0x65: ("Increment R0 by 14 and nibble swap.", reg_update),
        0x66: ("Increment R0 by 15 and nibble swap.", reg_update),
        0x6C: ("Load byte from register (R2) to R0.", reg_update),
        0x6E: ("Increment Address Register R1.", None),
        0x70: ("Decrement register (R1).", None),
        0x70: ("Print register (R1).", None),
        0x73: ("Store byte R0 to register (R1).", None),
        0x75: ("Update RAM pointers R3,R4 to R9,R10.", None),
        0x7C: ("Transmit byte in R18 to POD IO-0.", None),
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

registers = [None] * len(BitScope.registers)


def reset():
    registers = [0] * len(BitScope.registers)

def version():
    s.write('\r')
    s.write(BitScope.versions[7])
    s.write('\r')

def reg_update(cmd):
    register[0] += (cmd & 0xf)
    register[0] = register[0] + 4;
    print hex(register[0])


s = serial.Serial('uart2')

while True:
    char = s.read(1)

    # Print received command
    cmd = ord(char)
    print hex(cmd),

    # Get handler
    f = bytecode[cmd][2]

    if f is None:
        print '???'
    else:
        print bytecode[ord(char)]

    f(cmd)

    # Send command back when it has been executed
    s.write(char)
