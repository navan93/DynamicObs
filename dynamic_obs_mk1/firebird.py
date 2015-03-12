import serial,binascii,struct

ser = serial.Serial('/dev/ttyS0',baudrate=57600,stopbits=1,parity='N',timeout=0.3)

ser.close()
ser.open()
ser.flush()

#nex='\x4e\x45\x58'

def move(left_velocity,right_velocity):
	
	comm=0x94
	subc=0x01
	data=struct.pack('5B',0x4e,0x45,0x58,comm,subc)
	ser.write(data)
	print data

	comm=0x95
	subc=128-left_velocity
	data=struct.pack('5B',0x4e,0x45,0x58,comm,subc)
	ser.write(data)
	print repr(data)	

	comm=0x96
	subc=128-right_velocity
	data=struct.pack('5B',0x4e,0x45,0x58,comm,subc)
	ser.write(data)
	print data
	
def stop():
	move(0,0)

def safety(mode):
	
	comm=0x89
	subc=mode
	data=struct.pack('5B',0x4e,0x45,0x58,comm,subc)
	#data='\x4e\x45\x58\x20\x00'
	ser.write(data)
	print data

	


