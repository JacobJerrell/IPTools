"""
IP Address Tools
"""
### This is an old file.
# Some of the calculations need to be
# incorporated into IPTools.py
# Then this file can be deleted
import pprint as pprint

IPInfo = {}

NONBINARY = '23456789'
JUNK = " \t\n\r\v\fabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ""!""#$%&'()*+,-/:;<=>?@[\]^_`{|}~"""

def toBinary(ip):
    if any((c in JUNK) for c in ip):
        print('You\'re doing it wrong.')
        print('Expected: 0-9')
        print('Got: Something else.')
        print('toBinary()')
        quit()
    # IPInfo['binaryIP'] = ''.join([bin(int(x)+256)[3:] for x in ip.split('.')])
    inBinary = ''.join([bin(int(x)+256)[3:] for x in ip.split('.')])
    while len(inBinary) < 32:
        inBinary = inBinary + '0'
    return inBinary

def toDecimal(ip):
    if any((d in NONBINARY) for d in ip) or any((c in JUNK) for c in ip):
        print('You\'re doing it wrong.')
        print('Expected: 0\'s and 1\'s.')
        print('Got: Something else.')
        print('toDecimal()')
        quit()
    while len(ip) < 32:
        ip = ip + '0'
    if '.' in ip:
        octets = ip.split('.')
    else:
        octets = [ip[i:i+8] for i in range(0, len(ip), 8)]

    decimalIP = ''
    for x in octets:
        bits = list(enumerate(x)) # Make it a tuple
        rolling = 0               # Initialize counter
        for i, digit in bits:     # Loop through the tuple
            if digit == '1':      # Find the decimal equivalent based
                                  # on its location in the tuple:
                number = 2**(7-i)
                # Add it to the rolling balance:
                rolling = rolling + number
        decimalIP = decimalIP + '.' + str(rolling)
    return decimalIP[1:]
    # IPInfo['IP'] = decimalIP[1:]

def _calcMask(wack):
    if any((c in JUNK) for c in str(wack)) or int(wack) > 32:
        print('You\'re doing it wrong!\nExpected: 0-32\nGot: Something else')
        print('_calcMask()')
        quit()
    mask = ''
    wack = int(wack)
    while wack:
        mask = mask + '1'
        wack -= 1
    while len(mask) < 32:
        mask = mask + '0'
    return mask

def _countMaskBits(mask):
    if '.' in mask:
        mask = toBinary(mask)
    while len(mask) < 32:
        mask = mask + "0"
    return mask.count('1')

def _calcNetworks(wack):
    maskBits = int(wack)
    maxSubnets = 2**(32-maskBits)
    maxHosts = 2**(32-maskBits) - 2
    return maxSubnets, maxHosts

def _calcNetID(ip, wack):
    IP = toBinary(ip)
    netID = IP[:int(wack)]
    while len(netID) < 32:
        netID = netID + '0'
    netID = toDecimal(netID)
    return netID

def _calcNetRange(ip, wack):
    startIP = toBinary(_calcNetID(ip, wack))
    endIP = startIP[:int(wack)]
    while len(endIP) < 32:
        endIP = endIP + '1'
    startIP = toDecimal(startIP)
    endIP = toDecimal(endIP)
    return startIP, endIP

def start(ip, wack):
    IPInfo['ip'] = ip
    IPInfo['binaryIP'] = toBinary(ip)
    IPInfo['binaryMask'] = _calcMask(wack)
    IPInfo['mask'] = toDecimal(IPInfo['binaryMask'])
    IPInfo['subnets'] = _calcNetworks(wack)[0]
    IPInfo['hosts'] = _calcNetworks(wack)[1]
    IPInfo['NetworkID'] = _calcNetID(ip, wack)
    IPInfo['CIDRNotation'] = IPInfo['NetworkID'] + "/" + str(wack)
    IPInfo['CIDRRange'] = _calcNetRange(ip, wack)
    return IPInfo

if __name__ == '__main__':
    print('#################################################################################')
    print('IP Tools by J. Jerrell 11/17')
    print('Desc: Contains tools that may be used individually, or')
    print('      start(ip, wack) will give as much info as possible.')
    print('#################################################################################\n')
    print('1. Dotted Decimal to Binary Conversion     2. Binary to Dotted Decimal Conversion')
    print('3. Convert wack masks to decimal masks     4. Convert decimal masks to wack masks')
    print('5. Calculate Networks, Hosts, and Range    6. Determine network ID')
    print('7. Get all possible info')
    decide = input("Make your selection: ")
    if decide == '1':
        print(toBinary(input("Enter the IP Address to Convert: ")))
    elif decide == '2':
        print(toDecimal(input("Enter the binary address to Convert: ")))
    elif decide == '3':
        print(_calcMask(input("Enter the wack (0-32): ")))
    elif decide == '4':
        print(_countMaskBits(input("Enter the mask: ")))
    elif decide == '5':
        IPArg = input("Enter the IP Address: ")
        MaskArg = input("Enter the mask: ")
        if '.' in MaskArg:
            MaskArg = toBinary(MaskArg)
        MaskArg = MaskArg.count('1')
        print('Subnets:  ' + str(_calcNetworks(MaskArg)[0]))
        print('Hosts:    ' + str(_calcNetworks(MaskArg)[1]))
        print('Range:    ' + _calcNetRange(IPArg, MaskArg)[0] + ' - ' + _calcNetRange(IPArg, MaskArg)[1])
    elif decide == '6':
        IPArg = input("Enter the IP Address: ")
        MaskArg = input("Enter the mask: ")
        print('Network ID: ' + _calcNetID(IPArg, MaskArg))
    elif decide == '7':
        IPArg = input("Enter the IP Address: ")
        MaskArg = input("Enter the mask: ")
        if '.' in MaskArg:
            MaskArg = toBinary(MaskArg)
            MaskArg = MaskArg.count('1')
        pprint.pprint(start(IPArg, MaskArg))

"""
if __name__ == '__main__':
    import timeit
    print(timeit.timeit("toDecimal('11010110000011101010111101011011')", setup="from __main__ import toDecimal"))
    print(timeit.timeit("uglytoDecimal('11010110000011101010111101011011')", setup="from __main__ import uglytoDecimal"))
"""
