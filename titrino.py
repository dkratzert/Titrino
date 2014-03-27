#!/usr/bin/env python
import os
import serial
import time
import re
import sys

comport = 4

ser = serial.Serial(port = '\\.\COM{}'.format(comport), baudrate=9600, timeout=1)
ser.close()
ser.open()


def write_command(data):
    try:
        ser.close()
        ser.open()
        ser.write(data)
        print(ser.readline())
        ser.close()
    except():
        pass


def read_status():
    try:
        ser.close()
        ser.open()
        ser.write('&M $D \r\n') #status
        print(ser.readline())
        ser.close()
    except():
        pass

def read_data(data, i):
    try:
        ser.close()
        ser.open()
        ser.write(data) #status
        time.sleep(1)
        ph = ser.readline().strip('\n\r"')
        #print('pH = {} | Zeit = {}'.format(ph, i))
        ser.close()
        return [ph, i]
    except():
        pass


  

start = '&M $G\r\n' # start der Messung

stop = '&M $S\r\n' # stop der messung

#messwerte = '&I.D.M $Q\r\n'
#messwerte = '&I.D.M.X $Q\r\n'
messwerte = '&I.A.T.M $Q\r\n' #pH


def write_file(ph_liste):
    write_command(stop) #stop der messung
    read_status()
    ser.close()
    name = raw_input("Bitte Probennamen eigeben: ") 
    try:
        outfile = open('{}.txt'.format(name), 'w')
    except:
        outfile = open('output.txt', 'w')
    outfile.write("pH  Zeit\n\n")
    for i in ph_liste:
        i = '  '.join(i)
        outfile.write("%s\n" %i)
    outfile.close()


#print('initialer status:')
#write_command(stop)
#time.sleep(0.05)
#read_status()

#print('starte messung:')
#write_command(start) # hier wird messung gestrtet




messdauer = 48 # in Stunden

messdauer = messdauer*60*60

ph_liste = []
L = []
#thread.start_new_thread(input_thread, (L,))

try:
    while 1:
        for i in range(messdauer):
            i = str(i)
            ph = read_data(messwerte, i)
            #if re.match('.*valid', ph[0]):
            #    continue
            print('pH = {} | Zeit = {}'.format(ph[0], i))
            ph_liste.append(ph)
except(KeyboardInterrupt):
    write_file(ph_liste)
    sys.exit()

