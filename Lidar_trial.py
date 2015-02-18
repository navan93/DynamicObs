import serial,binascii,struct
from operator import add,sub
import math

port= serial.Serial('/dev/ttyACM0',baudrate=115200,timeout=0.5)

port.close()
port.open()

md='\x4d\x44'
start_step='\x30\x31\x32\x37'
end_step='\x30\x31\x32\x39'
cluster='\x30\x31'
scan_int='\x30'
num_scans='\x30\x31'
lf='\x0a'

data=md+start_step+end_step+cluster+scan_int+num_scans+lf

print data

port.write(data)

resp=port.read(21)
print binascii.b2a_hex(resp)

resp=port.read(38)
print binascii.b2a_hex(resp)
resp_data=binascii.hexlify(resp[26:35])

a= list(struct.unpack('38B',resp))
b= [48]*9
res= map(sub,a[26:35],b)
print res
length=len(res)/3
dists=[0]*length
for i in range(len(res)/3):
	dists[i]+=res[i*3+0]*1000+res[i*3+1]*100+res[i*3+2]
print dists
