import lidar
import clustering
import time
import plotter
import Object_Avoid

dists = lidar.getscan(129,640,1) 
tstamp=time.time()

C1=clustering.meanshift(dists,tstamp)
#if C1!='fail':
#	plotter.plot(C1)

time.sleep(2)

dists = lidar.getscan(129,640,1) 
tstamp=time.time()

C2=clustering.meanshift(dists,tstamp)

#f C2!='fail':
	#plotter.plot(C2)
#ime.sleep(5)

Object_Avoid.avoid(C1[0],C2[0])