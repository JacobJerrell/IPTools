"""
IP Calculator is an experimental, and educational project.
Almost everything here can be done with modules from the
standard library. That being said, if you find something
useful here, feel free to use it however you like.
"""
# Import RegEx
import re

# Constants
NONBINARY = '23456789'
JUNK = " \t\n\r\v\fabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ""!""#$%&'()*+,-/:;<=>?@[\]^_`{|}~"""
IPV4_RE = re.compile('^(?:(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])(\\.(?!$)|$)){4}$')

################
# Error Handler
################
class Error(Exception):
    """Base class for exceptions in this module"""
    pass

class InputError(Error):
    """Exception raised for errors in the input.
    
    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error"""
    
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

#########
# Tests
#########
class ValidateInput(object):
    def __init__(self, arg):
        self.arg = arg
        self.junk = JUNK
        self.nonbinary = NONBINARY
        self.re = IPV4_RE
        self.junk = self.junk_finder(arg)
        self.ipv4 = self.valid_ipv4(arg)
        self.binary = self.valid_binary(arg)
        if self.junk:
            raise InputError(arg, 'Found invalid characters in provided string.')
            # self.validated = 'junk'
        elif self.ipv4:
            self.validated = 'ipv4'
        elif self.binary:
            self.validated = 'binary'
        else:
            raise InputError(arg, 'Something very wrong happened.')
    
    def junk_finder(self, arg):
        if any ((c in self.junk) for c in str(arg)):
            return True
        else:
            return False

    def valid_ipv4(self, arg):
        if self.re.match(str(arg)):
            return True
        else:
            return False

    def valid_binary(self, arg):
        if (any((d in self.nonbinary) for d in arg) or
                len(arg) > 32):
            return False
        else:
            return True

###########
# Do work
###########
class HandleInput(ValidateInput):
    def __init__(self, arg):
        super().__init__(arg)
        self.arg = arg
        if self.validated == 'ipv4':
            self.inDecimal = self.arg
            self.inBinary = self.toBinary(arg)
        elif self.validated == 'binary':
            self.inDecimal = self.toDecimal(arg)
            while len(self.arg) < 32:
                self.arg = self.arg + '0'
            self.inBinary = self.arg

    def toDecimal(self, arg):
        while len(arg) < 32:
            arg = arg + '0'
        if '.' in arg:
            arg.strip('.')
        octets = [arg[i:i+8] for i in range(0, len(arg), 8)]
        decimal_ip = ''
        for x in octets:
            bits = list(enumerate(x))
            rolling = 0
            for i, digit in bits:
                if digit == '1':
                    number = 2**(7-i)
                    rolling = rolling + number
            decimal_ip = decimal_ip + '.' +str(rolling)
        return decimal_ip[1:]

    def toBinary(self, arg):
        binary = ''.join([bin(int(x)+256)[3:] for x in arg.split('.')])
        while len(binary) < 32:
            binary = binary + '0'
        return binary
        

# def interpret(arg, expected):
#     # First check for invalid characters:
#     if any((c in JUNK) for c in arg):
#         print('Found invalid character.')
#         return False
#     # Test for nonbinary digits
#     if expected == 'binary':
#         if any((d in NONBINARY) for d in arg):
#             print('Passed invalid char test. Failed binary test.')
#             return False
#         else:
#             print('Passed invalid char test. Passed binary test')
#             return True
#     if expected == 'decimal':
#         # Fix partial IP addresses
#         while len(arg.split('.')) < 4:
#             print('Had to add .0 to string')
#             arg = arg + '.0'
#         # Test for valid IPv4 address
#         if validIPv4(arg):
#             print('Passed invalid char test. Passed validIPv4 address test.')
#             return True
#         else:
#             print('Passed invalid char test. Failed validIPv4 address test.')
#             return False
#     # Test for valid wack format
#     if expected == 'wack':
#         if int(arg) > 32 or int(arg) < 0:
#             print('Passed invalid char test. Expected 0-32. Got something else')
#             return False
#         else:
#             return True

"""
# Test Interpret Function
# TODO: Major logic changes in the above code
interpret('a', 'binary') # Should fail invalid char test
interpret('a', 'decimal') # Should fail invalid char test
interpret('234', 'binary') # Should pass invalid char, and fail binary test
interpret('11111011101111', 'binary') # Should pass invalid char, and binary test
interpret('192.168.1.1', 'decimal') # Should pass invalid char, and decimal test
interpret('192.256.13.444', 'decimal') # Should pass invalid char, and fail decimal test
interpret('192.168', 'decimal') # Should pass invalid char, and pass IPv4 Test
"""
# Testing the process of splitting /24 type arguments
'''
slash = argument.split('/')
print(slash)
octets = slash[0].split('.')
print(octets)
slashMask = int(slash[1])
print(type(slashMask))
mask = ""
while slashMask:
    mask = mask + "1"
    slashMask -= 1
if len(mask) < 32:
    add = 32 - len(mask)
    while add:
        mask = mask + "0"
        add -= 1

print(mask)
'''

# From old file. Extra the 'wack' logic. discard the rest
# def simplifyIP(ip):
#     # Check for wack
#     if '/' in ip:
#         separate = ip.split('/')        # separate[0] = everything before the wack
#                                         # separate[1] = everything after the wack
#         IPInfo['ip'] = separate[0]      # Assign the dotted decimal IP to the IPInfo dict
#         # Prepare to make the mask
#         maskBits = int(separate[1])     # Make the str an int
#         wackLogic(maskBits)             # Pass it to wackLogic to build the mask
#         ip = IPInfo['ip']
#     if len(ip.split('.')) <= 4:
#         octets = ip.split('.')          # Find the octets
#         while len(octets) < 4:          # Handle partial IPs
#             octets.append('0')
#         IPInfo['ip'] = '.'.join(octets)
#     IPInfo['binaryIP'] = toBinary(IPInfo['ip'])

# def toBinary(arg):
#     if interpret(arg, 'decimal'):
#         return ''.join([bin(int(x)+256)[3:] for x in arg.split('.')])

# interpret('192.168.1.1', 'binary')
# print(toBinary('16.23'))