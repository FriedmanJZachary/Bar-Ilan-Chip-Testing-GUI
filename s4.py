import sys
sys.path.insert(0, "/opt/rh/rh-python36/root/usr/lib/python3.6/site-packages")
import serial

#Serial connection to voltage supply
ser = serial.Serial(
    port='/dev/ttyUSB0',
    timeout=2,
    parity=serial.PARITY_NONE,
    stopbits=2,
    dsrdtr=1
)

#Writes a command directy to the supply
def wcom(cmd):
    cmd += '\n'
    ser.write(cmd.encode(encoding='ascii',errors='strict'))

#Sequentially shuts supply, sets voltage and current values, and turns the supply back on
def setSequence(rail,volt,curr):
    wcom('SYSTEM:REMOTE')
    wcom('OUTPUT:STATE ' + ('OFF'))
    wcom('APPL %s, %s, %s' % (rail,volt,curr))
    wcom('OUTPUT:STATE ' + ('ON'))

setSequence('P25V','2.0', '0.1')
