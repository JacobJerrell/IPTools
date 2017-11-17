'''
******************************************************
Originally created by C. Nichols #B0)~
Lives at:
https://github.com/ActiveState/code/blob/master/recipes/Python/162994_IPy_Notify/recipe-162994.py
******************************************************
Adapted to support Python 3, Windows, Linux, and OS X
Description: Monitors the devices Internal or external
             IP address for changes. If a change is
             detected, it is setup to send an email to
             a/an specified address(es)
******************************************************
'''
import os
import sys
import time
import smtplib
from email.message import EmailMessage
import socket

'''
The following lines should be modified to match your mail server
'''
MAILSERVER = 'smtp.yourprovider.com'
# Supports multiple email addresses:
ADDRESS = ['yourmail@yourprovider.com', 'othermail@yourprovider.com']
# The email address that will send the message:
FRM_ADD = 'yourmail@yourprovider.com'

# USER = '' # One day I may support this
# PASS = '' # One day I may support this

'''
Do we need the internal or external IP to be monitored?
'''
IPTYPE = input("(E)xternal or (I)nternal? ")

'''
The following if/elif/else will return the following important variables:
PATH_DAT = The location to the .dat file that the current IP will be stored in
PATH_LOG = The location to the .log file
NAME = The name of the computer

Alternatively, it will bomb if it doesn't detect an OS that it was prepared for
'''
if sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
    import win32api
    SYSDIR = os.path.split(win32api.GetSystemDirectory())
    LDRIVE = os.path.split(SYSDIR + 'IPyNotify')
    if not os.path.exists(LDRIVE):
        os.makedirs(LDRIVE)
    PATH_DAT = LDRIVE + 'IPy_Notify.dat'
    PATH_LOG = LDRIVE + 'IPy_Notify.log'
    NAME = win32api.GetComputerName()
elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    PATH = os.path.expanduser('~') + '/IPyNotify'
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    PATH_DAT = PATH + '/IPy_Notify.dat'
    PATH_LOG = PATH + '/IPy_Notify.log'
    NAME = socket.gethostname()
else:
    print("Apparently I wasn't prepared for your OS... sorry\nAborting Application")
    time.sleep(5)
    quit()

def mail():
    '''Builds, and sends the email in the event a new IP is detected'''
    msg = EmailMessage()
    msg['Subject'] = 'Message from ' + NAME
    msg['To'] = ', '.join(ADDRESS)
    msg['From'] = FRM_ADD
    msg.add_header('Content-Type', 'text')
    msg.set_content('New IP address: ' + NEW_IP + ' assigned to ' + NAME)
    try:
        with smtplib.SMTP(MAILSERVER) as s:
            s.send_message(msg)
    except:
        print('Error: Unable to send notification! - ' + time.ctime())
        open(PATH_LOG, 'a').write(time.ctime() + '\nError: Unable to send notification!')

def start():
    '''Contains the getIP and 'out' functions that make the whole thing work'''
    def getIP(name, path, kind):
        '''Seek the devices IP address'''
        print('IPy Notify v2.1 - Rewritten and expanded by J. Jerrell, 2017')
        if kind.upper() == 'E':
            import urllib.request
            import json
            EXTIP = json.loads(urllib.request.urlopen("http://ip.jsontest.com/").read())
            IP = EXTIP["ip"]
        elif kind.upper() == 'I':
            IP = socket.gethostbyname(name)

        print('Current IP: ' + str(IP))
        open(path, 'w').write(IP)
        out(name, path, kind)

    def out(name, path, kind, stat=1):
        '''Update the terminal, write to files, send email if needed'''
        while stat:
            CUR_IP = open(path, 'r').readline()
            if kind.upper() == 'E':
                import urllib.request
                import json
                EXTIP = json.loads(urllib.request.urlopen("http://ip.jsontest.com/").read())
                NEW_IP = EXTIP["ip"]
            elif kind.upper() == 'I':
                NEW_IP = socket.gethostbyname(name)
            if CUR_IP == NEW_IP:
                print('Sleeping...')
                time.sleep(15)
                print('Polling: ' + NEW_IP + ', ' + time.ctime())
            else:
                print('IP address has changed: ' + NEW_IP)
                open(PATH_LOG, 'a').write(time.ctime() + '\nINFO: IP address changed: ' + NEW_IP)
                print('Sending notification...')
                for add in ADDRESS:
                    mail()
                getIP(NAME, PATH_DAT, IPTYPE)
                stat = 0

    getIP(NAME, PATH_DAT, IPTYPE)

try:
    open(PATH_LOG, 'a').write(time.ctime() + ' START: IP Polling\n-------------------------')
    start()
except:
    open(PATH_LOG, 'a').write(time.ctime() + ' \nError: IPy Notify Failed!')
