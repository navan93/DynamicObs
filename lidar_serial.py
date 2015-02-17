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

def getscan(start,end,cluster):
	start_step = "%04d"%start
	end_step   = "%04d"%end
	cluster    = "%02d"%cluster
	scan_int   = "%01d"%0
	num_scans  = "%02d"%1
	lf         = '\x0a'
	data = struct.pack('16s',"MD",start_step,end_step,cluster,scan_int,num_scans,lf)
	print data
	port.write(data)

	resp1 = port.read(21)
	print binascii.b2a_hex(resp1)

	steps 	 = end-start+1
	data_len = steps*3
	quo 	 = data_len/64
	rem 	 = data_len%64

	if data_len<64:
		final_data_len = 29 + data_len
	if quo!=0 and rem==0
		final_data_len = 27 + 66*quo
	if quo!=0 and rem!=0
		final_data_len = 27 + 66*quo + rem + 2

	resp2 = port.read(final_data_len)
	lines=resp2.splitlines()
	del lines[0:4]
	del lines[-1]
	a = list()
	for line in lines:
		del line[-1]
		a+= list(struct.unpack(str(len(line))+'B',line))
	dec = [48]*data_len
	res=map(sub,a,dec)
	res_dists = map(sub,resp2,dec)
	print res
	length=len(res)/3
	dists=[0]*length
	for i in range(len(res)/3):
		dists[i]+=res[i*3+0]*1000+res[i*3+1]*100+res[i*3+2]
	print dists



