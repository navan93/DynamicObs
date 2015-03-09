import serial,binascii,struct
from operator import add,sub
import time
import math
import os

os.system('clear')
port= serial.Serial('/dev/ttyACM0',baudrate=115200,timeout=0.5)

port.close()
port.open()


b = list()

class obstacle(object):
	name = 0
	start =0
	end = 0
	radius = 0
	alpha = 0
	theta = 0

	def rad(self,reads,start,end):
		temp = reads[start:end+1]
		self.radius = min(temp)

	def __init__(self,start,end,name):
		self.name = name
		self.start = start
		self.end = end
		self.alpha = (end-start)*0.36
		self.theta = ((end+start)/2)*0.36 
 
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
#	print binascii.b2a_hex(resp1)

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
	#print binascii.hexlify(resp2)
	lines= resp2[26:-1].splitlines()
	#print len(lines)
	a=list()
	for line in lines:
		line=line[:-1]
		#print len(line)
		a+= list(struct.unpack(str(len(line))+'B',line))
	
	dec = [48]*len(a)
	res_dists = map(sub,a,dec)
	length=len(res_dists)/3
	dists=[0]*length
	for i in range(length):
		dists[i]=int(bin(res_dists[i*3+0])[2:].zfill(6)+bin(res_dists[i*3+1])[2:].zfill(6)+bin(res_dists[i*3+2])[2:].zfill(6),2)
	
	pos=list()
	diff=list()
	for k in range(len(dists)):
		if dists[k] > 20:
			pos.append(k)

	for k in range(len(pos)-1):
		diff.append(pos[k+1]-pos[k])

	final=list()

	for k in range(len(pos)-1):
		if diff[k]==1:		
			final.append(pos[k+1])
	clone= list()
	for k in range(len(final)):
		clone.append(dists[final[k]])
	count = 0
	spike = list()
	conti = 0
	spike.append(dists[final[0]])
	for k in range (len(final)-1):
		spike.append(abs(clone[k]-clone[k+1]))
		#print k,"  ",spike[k],"  ",clone[k],"  ",final[k]
	proceed = 0
	#print spike,"  ",len(spike)
	for k in range(len(spike)):
        	finish = 0
       		if spike[k] > 600:
    			begin = k
    		if (spike[k] < 30) and (spike[k-1] > 600):
    			proceed = 1
    		if (spike[k] < 30) and (proceed == 1):
    			conti = conti+1
    			#print "First  ",k,"  ",len(spike),"  ",conti
    		'''else:
    	   		conti = 0
    	   		proceed = 0'''

    	   	if conti > 19:
          		while spike[k-1] < 30 and k < len(spike):
          			#print k
          			conti = 0
          			proceed = 0
         		   	k+=1
        	     	finish = k
        	if finish != 0:
        		count+=1
        		proceed=0
        		print begin,"  ",finish
        		a = obstacle(final[begin],final[finish],count)
        		a.rad(clone,begin,finish)
        		b.append(a)
        		print a.name,"%4d"%a.start,"%4d"%a.end,"%4d"%a.radius,"%4d"%a.alpha,"%4d"%a.theta
            	k-=1
				 
	#print count

getscan(129,639,1)
#print len(b)
port.close()
#time.sleep(3)