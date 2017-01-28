#!/usr/bin/python

# Keypad doc: http://www.circuitstoday.com/interfacing-hex-keypad-to-arduino

import copy
import omega_gpio
import datetime
import time
import urllib2

a = [0,1,2,3,11,18,8,9]
r = [0,1,2,3]
c = [18,11,8,9]

key = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"],
]

values = [
    ["0", "0", "0", "0"],
    ["0", "0", "0", "0"],
    ["0", "0", "0", "0"],
    ["0", "0", "0", "0"],
    ["0", "0", "0", "0"],
]

lastvalues = copy.deepcopy(values)

# close before open if used 
for pin in a:
	try:
		omega_gpio.closepin(pin)
	except:
		e = 1 # dummy command :-)

# pin init
for pin in r:
	omega_gpio.initpin(pin,'out')

for pin in c:
	omega_gpio.initpin(pin,'in')

while True:
	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	rpos = 0
	for rpin in r:
		omega_gpio.setoutput(r[0], 0)
		omega_gpio.setoutput(r[1], 0)
		omega_gpio.setoutput(r[2], 0)
		omega_gpio.setoutput(r[3], 0)
		omega_gpio.setoutput(rpin, 1)
		time.sleep(0.05)
		cpos = 0
		for cpin in c:
			input = omega_gpio.readinput(cpin)
			values[rpos][cpos] = input
			cpos = cpos + 1
		rpos = rpos + 1
	
	for x in range(0, 4):
		for y in range(0, 4):
			if values[x][y] != lastvalues[x][y]:
				keycode = key[x][y]
				if values[x][y] == 1:
					print 'Key %s presed' % (keycode)
				else:
					print 'Key %s released' % (keycode)

	lastvalues = copy.deepcopy(values)


# release the pin
for pin in a:
	omega_gpio.closepin(pin)
