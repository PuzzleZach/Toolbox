#!/usr/bin/env python3
'''
Encoder/Decoder for on the fly command line conversions.
Usage: ./CodeConvert -[input] -[output] -[value]
Example: ./CodeConvert -hex -dec "14AC"
'''
import sys

#This function enables the calling of a variable. 
def callFunction(fn):
    fn()
    
#Dictionary for hex values.
hex = {"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9, "A": 10, "B": 11, "C":12, "D":13, "E":14, "F":15}
options = ["hex", "dec", "bin"]
#We use command line args to determine what to.
args = sys.argv
inputArg = args[1][1:] #Strip out the "-"
outputArg = args[2][1:]
value = args[3]

if inputArg not in options:
 print("Input form currently not supported. Please try again with one of the following:")
 print(x for x in options)
 sys.exit()
elif outputArg not in options:
 print("Output form currently not supported. Please try again with one of the following:")
 print(x for x in options)
 sys.exit()

funcCall = "{}to{}(\"{}\")".format(inputArg.title(), outputArg.title(), value) 
print(funcCall)
#callFunction(funcCall)

def HexToDec(val):
    if val[0] != "x":
        print("Please enter a valid hex numer!")
        HexToDec()
    total = 0
    for i, value in enumerate(val[1:]):
        if value in hex:
            total += hex.get(value) * (16**(len(val[1:])-i-1))
    print(total)
    
def DecToHex(val):
    total = []
    final = ""
    while val > 0:
        total.append(val%16)
        val = val // 16
    total.reverse()
    
    for i in total:
        for j in hex:
            if hex.get(j) == i:
                final += str(j)
    print(final)
            
