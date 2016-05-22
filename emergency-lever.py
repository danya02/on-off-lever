#!/usr/bin/python
import RPi.GPIO as gpio
import paramiko 
import json
import time
from wakeonlan import wol
global val
val=True
global ticks
ticks=0
gpio.setmode(gpio.BOARD)
conf=json.load(open("config.json"))
gpio.setup(conf["on-pin"],gpio.IN,gpio.PUD_UP)
gpio.setup(conf["off-pin"],gpio.IN,gpio.PUD_UP)
gpio.setup(40,gpio.OUT)
gpio.output(40,True)
def xoff(void):
	if ticks==0:
		ticks=ticks+20
		print("XOFF event")
		val=True
		gpio.output(40,False)
		for i in conf["hosts"]:
			client = paramiko.SSHClient()
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			client.connect(hostname=i["host"], username=i["user"], password=i["pass"], port=22)
			client.exec_command('poweroff')
			client.close()
			client=None
def xon(void):
	if ticks==0:
		ticks==ticks+20
		print("XON event")
		val=True
		gpio.output(40,True)
		for i in conf["hosts"]:
			wol.send_magic_packet(i["mac"])
gpio.add_event_detect(conf["on-pin"],gpio.FALLING,xon)
gpio.add_event_detect(conf["off-pin"],gpio.FALLING,xoff)
while 1:
	time.sleep(1)
	if ticks!=0:ticks=ticks-1
	
