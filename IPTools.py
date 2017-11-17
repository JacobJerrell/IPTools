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
JUNK = " \t\n\r\v\fabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ""!""#$%&'()*+,-:;<=>?@[\\]^_`{|}~"""
IPV4_RE = re.compile('^(?:(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])(\\.(?!$)|$)){4}$')

################
# Error Handler
################
class Error(Exception):
    """Base class for exceptions in this module"""
    pass

class InputError(Error):
    """Exception raised for errors in the input.
    
    Args:
        expression: input expression in which the error occurred
        message: explanation of the error"""
    
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

#########
# Tests
#########
class ValidateInput(object):
    """Validates the users input.

    Receives the string that was passed to the HandleInput class, runs
    various tests to confirm the validity of the string. Also determines
    whether a binary, dotted decimal, or dotted decimal + wack was passed

    Args:
        arg: A string containing <= 32 1's/0's
             A string containing an IPv4 address (192.168.1.1)
             A string containing an IPv4/wack address (192.168.1.1/24)
    
    Returns:
        Nothing. It sets several self variables for use in the HandleInput
        class
    
    Raises:
        InputError: An error occurred because an invalid string was passed.
    """
    def __init__(self, arg):
        self.arg = arg
        # Handle wack addresses (192.168.1.1/24):
        if '/' in self.arg:
            self.wack = self.arg.split('/')[1]
            self.arg = self.arg.split('/')[0]
        self.junk = JUNK
        self.nonbinary = NONBINARY
        self.reg = IPV4_RE
        self.junk = self.junk_finder(self.arg)
        self.ipv4 = self.valid_ipv4(self.arg)
        self.binary = self.valid_binary(self.arg)
        # Decide what type of argument we were passed
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
        """Looks for invalid characters in the arg

        Returns:
            True if junk is found
            False if junk is not found
        """
        if any ((c in self.junk) for c in str(arg)):
            return True
        else:
            return False

    def valid_ipv4(self, arg):
        """Determines if the arg is a valid IPv4 address

        Returns:
            True if the IPv4 address is valid
            False if the IPv4 address is invalid
        """
        if self.reg.match(str(arg)):
            return True
        else:
            return False

    def valid_binary(self, arg):
        """Determines if the arg is a valid IPv4 binary representation

        Returns:
            True if the argument is a valid IPv4 binary expression
            False if the argument is an invalid IPv4 binary expression
        """
        if (any((d in self.nonbinary) for d in arg) or
                len(arg) > 32):
            return False
        else:
            return True

###########
# Do work
###########
class HandleInput(ValidateInput):
    """Main class of the module. Handles the user's input

    Passes the argument to ValidateInput, and acts accordingly

    Args:
        arg: A string containing <= 32 1's/0's
             A string containing an IPv4 address (192.168.1.1)
             A string containing an IPv4/wack address (192.168.1.1/24)
    
    Returns:
        inDecimal: The argument, converted to decimal
        inBinary: The argument, converted to binary

        Additionally if wack was included, the following will be available
        binaryMask
        decimalMask
        network_info (max hosts, max subnets)
        network_id
        network_range (first IP, last IP - Does not include gateway, or broadcast)
        network_stats: Dictionary containing all of these methods (not inDecimal
                       or inBinary)
    """
    # TODO: Document the rest of the methods

    def __init__(self, arg):
        self.arg = arg
        super().__init__(self.arg) # Inherit declarations from ValidateInput
        # Set variables depending on the detected input
        if self.validated == 'ipv4':
            self.inDecimal = self.arg
            self.inBinary = self.toBinary(self.arg)
        elif self.validated == 'binary':
            self.inDecimal = self.toDecimal(self.arg)
            while len(self.arg) < 32:
                self.arg = self.arg + '0'
            self.inBinary = self.arg
        # We can do a lot more if an IP and a Wack was passed
        if self.wack:
            self.binaryMask = self.toMask(self.wack)
            self.decimalMask = self.toDecimal(self.binaryMask)
            self.network_info = self._calcNetworks(self.wack)
            self.network_id = self._calcNetID(self.inBinary, self.wack)
            self.network_range = self._calcNetRange(self.wack)
            self.network_stats = {'MaxSubnets': self.network_info[0],
                                  'MaxHosts': self.network_info[1],
                                  'Network ID': self.network_id,
                                  'First IP': self.network_range[0],
                                  'Last IP': self.network_range[1]}

    def toDecimal(self, arg):
        arg = str(arg)
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
    
    def toMask(self, wack):
        wack = int(wack)
        binary_mask = ''
        while wack > 0:
            binary_mask = binary_mask + '1'
            wack -= 1
        while len(binary_mask) < 32:
            binary_mask = binary_mask + '0'
        return binary_mask

    def _calcNetworks(self, wack):
        maskBits = int(wack)
        maxSubnets = 2**(32-maskBits)
        maxHosts = 2**(32-maskBits) - 2
        NetInfo = [maxSubnets, maxHosts]
        return maxSubnets, maxHosts

    def _calcNetID(self, ip, wack):
        netID = ip[:int(wack)]
        while len(netID) < 32:
            netID = netID + '0'
        return self.toDecimal(netID)

    def _calcNetRange(self, wack):
        # This seems really narly...
        binary_id = self.toBinary(self.network_id)
        startIP = int(binary_id)
        startIP = self.toDecimal(startIP)
        octets = startIP.split('.')
        octets[3] = int(octets[3]) + 2
        octets[3] = str(octets[3])
        startIP = '.'.join(octets)
        endIP = binary_id
        endIP = endIP[:int(wack)]
        while len(endIP) < 32:
            endIP = endIP + '1'
        endIP = int(endIP) - 1
        endIP = self.toDecimal(str(endIP))
        return startIP, endIP
