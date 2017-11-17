'''
*********************************************
Originally created by C. Nichols #B0)~
Lives at:
https://github.com/ActiveState/code/blob/master/recipes/Python/162994_IPy_Notify/recipe-162994.py
Adapted by J. Jerrell
Adapted to Version: Python 3+
Adapted to Support: Windoze, Linux, OS X
Desc: IPy Notify
Use: To notify whomever that your IP address
     has changed if you have a non-static IP
     and run a web server, game server, etc.
Email: Currently supports sending mail via
       local mailserver with no auth
*********************************************
As another note, it seems like the previous
script would only return the local IP and not
the external IP anyway. My commands for pulling
the IP are basically the same, and I only get a
10/8, 172/16, or 192/24 address depending on where
I run it from. I'm using OS X. Still need to test
on my PC
*********************************************
'''
# Import libraries to help with sys identification
import os
import sys

# For timestamps
import time

# For sending the email(s)
import smtplib
from email.message import EmailMessage
import socket

# Detect platform and determine/define necessary paths
if sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
    # Windoze Stuff
    import win32api
    HEAD = os.path.split(win32api.GetSystemDirectory()) # Get the win/sysdir path
    LDRIVE = os.path.split(HEAD) # Now get the local drive

    # The path will generally be c:\
    if not os.path.exists(LDRIVE + 'IPyNotify'):
        os.makedirs(LDRIVE + 'IPyNotify')

    PATH_DAT = LDRIVE + 'IPyNotify\\IPy_Notify.dat' # Program requires this file to run properly
    PATH_LOG = LDRIVE + 'IPyNotify\\IPy_Notify.log'
    # Uncomment and modify the next line, or modify the line above to put the log in a sub-directory
    #PATH_LOG = ldrive+'\yourdir\IPy_Notify.log'

    # Get the actual machine name
    NAME = win32api.GetComputerName()

    # Some testing stuff
    print('You\'re running ' + sys.platform)
    print('Your system directory is: ' + HEAD)
    print('Your local drive is : ' + LDRIVE)
    print('Dat file is located here: ' + PATH_DAT)
    print('Logs will be written here: ' + PATH_LOG)
    print('Your computers name is: ' + NAME)

elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    # OS X / Linux Stuff
    PATH = os.path.expanduser('~') + '/IPyNotify'
    if not os.path.exists(PATH):
        os.makedirs(os.path.expanduser('~') + '/IPyNotify')

    PATH_DAT = PATH + '/IPy_Notify.dat'
    PATH_LOG = PATH + '/IPy_Notify.log'
    # The next line may need improved. See:
    # https://stackoverflow.com/questions/4271740/how-can-i-use-python-to-get-the-system-hostname
    NAME = socket.gethostname()
    #PATH_DAT = os.path.expanduser('~') + '/subdir/IPy_Notify.dat' # Optional subdirectories
    #PATH_LOG = os.path.expanduser('~') + '/subdir/IPy_Notify.log' # Optional subdirectories

    # Test to make sure it works... it did
    print("Computer name is " + NAME)
    print("Dat file is located at: " + PATH_DAT)
    print("Log file is located at: " + PATH_LOG)
else:
    # Foreign / Unsupported OS
    print("Unsupported OS. User Species = Time Traveller \n Aborting Application")
    time.sleep(5)
    quit()

# Add your server name, mail server, and email addresses receiving notification
MAILSERVER = 'smtp.yourprovider.com'
ADDRESS = ['yourmail@yourprovider.com']
# Multiple addresses - uncomment will override above, or just modify the above line to match
#ADDRESS = ['yourmail@yourprovider.com','othermail@otherprovider.com']
FRM_ADD = 'yourmail@yourprovider.com'

'''
# If mailserver requires auth, leave blank and test if unsure
10/26 - Commenting out. currently working on a localhost only solution.
        Will work on implementing this in case people actually want to put
        un/pw in plain text
#USER = ''
#PASS = ''
'''

# Start constructing the email message
#def mail(recip='', frm='', subj='', body='', server=''):
def mail():
    ''' This is a docstring '''
    msg = EmailMessage()
    msg['Subject'] = 'Message from ' + NAME
    msg['To'] = ', '.join(ADDRESS)
    msg['From'] = FRM_ADD
    msg.add_header('Content-Type', 'text')
    msg.set_content('New IP address: '+ NEW_IP +' assigned to '+ NAME)
    try:
        with smtplib.SMTP('localhost') as s:
            s.send_message(msg)
    except:
        print('Error: Unable to send notification! - ' + time.ctime())
        open(PATH_LOG, 'a').write(time.ctime() + '\nError: Unable to send notification!')

def start():
    ''' Actually runs the program '''
    def getIP(name, path):
        ''' Aptly named '''
        print('IPy Notify v2.0 - Rewritten and expanded by J. Jerrell, 2017')
        IP = socket.gethostbyname(NAME)
        print('Current IP: ' + str(IP))
        open(path, 'w').write(IP) # Save the current IP address to the .dat file
        out(name, PATH_DAT)

    def out(name, path, stat=1):
        ''' This is also a docstring '''
        while stat:
            CUR_IP = open(path, 'r').readline()
            NEW_IP = str(socket.gethostbyname(NAME))
            if CUR_IP == NEW_IP:
                print('Sleeping...')
                time.sleep(15) # Sleep in seconds - adjust polling interval to your taste
                print('Polling: ' + NEW_IP + ', ' + time.ctime())
            else:
                print('IP address has changed: ' + NEW_IP)
                open(PATH_LOG, 'a').write(time.ctime() + '\nINFO: IP address changed: ' + NEW_IP)
                print('Sending notification...')
                for add in ADDRESS:
                    mail()
                getIP(NAME, PATH_DAT)
                stat = 0

    getIP(NAME, PATH_DAT)

# Run ------------------------
# Make sure to start via command line,
# via .cmd file in startup, or terminal
# Download Python @ www.python.org or PythonWin

try:
    open(PATH_LOG, 'a').write(time.ctime() + ' START: IP Polling\n------------------------------------------\n')
    start()
except:
    open(PATH_LOG, 'a').write(time.ctime() + ' \nError: IPy Notify Failed!')
