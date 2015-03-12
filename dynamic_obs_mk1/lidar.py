import serial
import binascii
import struct
from operator import add,sub
import math
import subprocess


output=subprocess.Popen(["dmesg"],stdout=subprocess.PIPE).communicate()[0]
output=output.split("\n")[::-1]

st='ttyACM0'

for i in range(len(output)):
	if output[i].find("Manufacturer: Hokuyo Data Flex for USB")!=-1:
		st=output[i-1]
		st=st[st.find("tty"):st.find("tty")+7]
		print st
		break
	

port = serial.Serial('/dev/'+st,baudrate=115200,timeout=0.5)
print "serial opened"
port.flushInput()
port.flushOutput()

def reset_lidar():
	data = '\x52\x53\x0a'
	port.write(data)
	resp = port.read(8)
	print resp

def getscan(start,end,cluster):

	
	start_step = "%04d"%start
	end_step   = "%04d"%end
	cluster    = "%02d"%cluster
	scan_int   = "%01d"%0
	num_scans  = "%02d"%1
	lf         = '\x0a'
	data = struct.pack('16s',"MD"+start_step+end_step+cluster+scan_int+num_scans+lf)
	print data
	port.write(data)

	
	resp1 = port.read(21)

	steps 	 = end-start+1
	data_len = steps*3
	quo 	 = data_len/64
	rem 	 = data_len%64

	if data_len<64:
		final_data_len = 29 + data_len
	if quo!=0 and rem==0:
		final_data_len = 27 + 66*quo
	if quo!=0 and rem!=0:
		final_data_len = 27 + 66*quo + rem + 2

	resp2 = port.read(final_data_len)
	print port.inWaiting()
	lines= resp2[26:-1].splitlines()
	
	a=list()
	for line in lines:
		line=line[:-1]
		a+= list(struct.unpack(str(len(line))+'B',line))
	
	dec = [48]*len(a)
	res_dists = map(sub,a,dec)
	length=len(res_dists)/3
	dists=[0]*length
	
	for i in range(length):
		dists[i]=int(bin(res_dists[i*3+0])[2:].zfill(6)+bin(res_dists[i*3+1])[2:].zfill(6)+bin(res_dists[i*3+2])[2:].zfill(6),2)

	return dists


