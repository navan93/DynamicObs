import math

def avoid(C1,C2):
	
	x1m=C1['center'][0]
	y1m=C1['center'][1]
	x2m=C2['center'][0]
	y2m=C2['center'][1]
	x2min=C2['xmin'][0]
	y2min=C2['xmin'][1]
	x2max=C2['xmax'][0]
	y2max=C2['xmax'][1]
	t1=C1['tstamp']
	t2=C2['tstamp']
	t=t2-t1
	alpha=math.degrees(abs(math.atan2(x2max,y2max)-math.atan2(x2min,y2min)))
	beta=math.degrees(abs(math.atan2(y1m-y2m,x1m-x2m)-math.atan2(y2m,x2m)))
	d=math.sqrt((x2m-x1m)**2+(y2m-y1m)**2)/1000
	v=d/t
	print 'alpha=',alpha,'beta=',beta,'v=',v,'dist=',d

	if alpha > beta:
		print "left"

