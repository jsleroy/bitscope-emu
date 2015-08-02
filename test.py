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
        0x00: "Reset the Virtual Machine. Print the Byte-Code number.",
        0x3F: "Print the 8 character string identifying the revision.",
        0x5B: "Clear R0. Usually commences byte entry.",
        0x30: "Increment R0 by 0 and nibble swap.",
        0x31: "Increment R0 by 1 and nibble swap.",
        0x32: "Increment R0 by 2 and nibble swap.",
        0x33: "Increment R0 by 3 and nibble swap.",
        0x34: "Increment R0 by 4 and nibble swap.",
        0x35: "Increment R0 by 5 and nibble swap.",
        0x36: "Increment R0 by 6 and nibble swap.",
        0x37: "Increment R0 by 7 and nibble swap.",
        0x38: "Increment R0 by 8 and nibble swap.",
        0x39: "Increment R0 by 9 and nibble swap.",
        0x61: "Increment R0 by 10 and nibble swap.",
        0x62: "Increment R0 by 11 and nibble swap.",
        0x63: "Increment R0 by 12 and nibble swap.",
        0x64: "Increment R0 by 13 and nibble swap.",
        0x65: "Increment R0 by 14 and nibble swap.",
        0x66: "Increment R0 by 15 and nibble swap.",
        0x5D: "Swap nibbles in R0. Usually concludes byte entry.",
        0x40: "Set Address Register R1.",
        0x23: "Set Source Address Register R2.",
        0x73: "Store byte R0 to register (R1).",
        0x6C: "Load byte from register (R2) to R0.",
        0x6E: "Increment Address Register R1.",
        0x70: "Print register (R1).",
        0x2B: "Increment register (R1).",
        0x70: "Decrement register (R1).",
        0x3C: "Capture Spock Counter to R9,R10.",
        0x3E: "Program Spock Registers from R3...R7.",
        0x54: "Trace until trigger + delay, then print Spock Counter.",
        0x44: "Delay until trigger and Trace, then print Spock Counter.",
        0x4C: "Trace Logic until trigger, then print Spock Counter.",
        0x53: "Sample dump (CSV format, analogue & digital data).",
        0x4D: "Mixed memory dump (Binary format, analogue & digital data).",
        0x45: "Scan for Event, then print Spock Counter.",
        0x41: "Analog memory dump (Binary format, analogue data).",
        0x50: "Measure time Period.",
        0x75: "Update RAM pointers R3,R4 to R9,R10.",
        0x7C: "Transmit byte in R18 to POD IO-0.",
        0x52: "Read EEPROM byte at address (R17) and print.",
        0x57: "Write byte R16 to EEPROM address (R17).",
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

s = serial.Serial('/home/jean-sebastien/COM2')

registers = [0] * len(BitScope.registers)

while True:
    char = s.read(1)
    print hex(ord(char)),
    try:
        print bytecode[ord(char)]
    except:
        print '???'
    s.write(char)

    if char == '?':
        s.write('\r')
        s.write(BitScope.versions[7])
        s.write('\r')
