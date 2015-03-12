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

def get():
	
	comm=0x89
	subc=0x00
	data=struct.pack('5B',0x4e,0x45,0x58,comm,subc)
	#data='\x4e\x45\x58\x20\x00'
	ser.write(data)
	print data

	s=binascii.hexlify(ser.read(50))
	str={'hdr':s[0:6],'comm':s[6:8],'subc':s[8:10],'data':s[10:]}
	print str




