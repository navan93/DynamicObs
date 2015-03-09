import serial,binascii,struct
from operator import add,sub
import math
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from cluster import HierarchicalClustering
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
import time

np.set_printoptions(threshold='nan')

port= serial.Serial('/dev/ttyACM1',baudrate=115200,timeout=0.3)

port.close()
port.open()
port.flush()

def getscan(start,end,cluster):

	start_step = "%04d"%start
	end_step   = "%04d"%end
	cluster    = "%02d"%cluster
	scan_int   = "%01d"%0
	num_scans  = "%02d"%1
	lf         = '\x0a'
	data 	   = "MD"+start_step+end_step+cluster+scan_int+num_scans+lf
	data 	   = struct.pack('16s',data)
	print data
	port.write(data)

	resp1 = port.read(21)
	#print binascii.b2a_hex(resp1)

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
	#print dists
	print dists

	X=list()
	Y=list()
	Z=list()
	theta=0

	for r in dists:
		X.append(r*math.cos(theta))
		Y.append(r*math.sin(theta))
		Z.append([r*math.cos(theta),r*math.sin(theta)])
		theta+=0.00628318531
	
	#print Z
	Z = np.array(Z)
	#print Z
	Z = Z[Z.all(1)]
	A=Z
	#print Z
	
	#plt.show()
	# plt.axis([-3500,3500,-3500,3500])
	# plt.ion()
	# plt.show()

	
	#Z = StandardScaler().fit_transform(Z)
	
	
	db = DBSCAN(eps=200, min_samples=10).fit(Z)
	
	core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
	
	core_samples_mask[db.core_sample_indices_] = True
	
	labels = db.labels_
	
	#print labels
	#print set(labels)
	
	# Number of clusters in labels, ignoring noise if present.
	n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
	print n_clusters_
	
	


	unique_labels = set(labels)
	
	colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
	C={}
	for k, col in zip(unique_labels, colors):
		if k == -1:
			col = 'k'

		class_member_mask = (labels == k)
		
		xy1 = A[class_member_mask & core_samples_mask]
		plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,markeredgecolor='k', markersize=14)
		
		xy2 = A[class_member_mask & ~core_samples_mask]
		plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,markeredgecolor='k', markersize=6)
		C[k]=np.concatenate(xy1,xy2)
	
	plt.title('Estimated number of clusters: %d' % n_clusters_)
	 
	
	plt.plot(Z[:,0],Z[:,1],'r.')
	
	plt.show()
	

getscan(127,640,1)
port.close()



