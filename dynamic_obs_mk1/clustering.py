import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
import math


np.set_printoptions(threshold=np.nan,precision=4,suppress=True)



def meanshift(dists,tstamp,range=2000):
	
		
	
	Z=list()
	C={}
	theta=0

	for r in dists:
		if r<10 or r>range:
			r=0
		Z.append([r*math.cos(theta),r*math.sin(theta)])
		theta+=0.00628318531
	Z = np.array(Z)
	
	Z=Z[Z.all(1)]
	
	# Compute clustering with MeanShift
	# The following bandwidth can be automatically detected using
	#bandwidth = estimate_bandwidth(Z, quantile=0.2)
	#print "bandwidth:",bandwidth
	
	ms = MeanShift(bandwidth=400, bin_seeding=True,cluster_all=True)
	try:
		ms.fit(Z)
	except:
		return 'fail'
	
	labels = ms.labels_
	cluster_centers = ms.cluster_centers_
	
	labels_unique = np.unique(labels)
	n_clusters_ = len(labels_unique) - (1 if -1 in labels else 0)
	
	for k in labels_unique:
		my_members = labels == k
		cluster_center = cluster_centers[k]
		cords=Z[my_members]
		C[k]={'center':cluster_center,'cords':cords,'xmin':cords[cords.argmin(axis=0)[0]],'xmax':cords[cords.argmax(axis=0)[0]],'flag':0,'tstamp':tstamp}
	
	return C


	
	
	





