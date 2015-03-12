import math

def avoid(C1,C2):
	vb=0.3
	dw=0
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
	alpha  = math.degrees(abs(math.atan2(x2max,y2max)-math.atan2(x2min,y2min)))
	theta1 = math.degrees(math.atan2(y1m-y2m,x1m-x2m))
	theta2 = math.degrees(math.atan2(y2m,x2m))
	theta3 = math.degrees(math.atan2(y1m,x1m))
	beta=abs(theta1-theta2)
	d=math.sqrt((x2m-x1m)**2+(y2m-y1m)**2)/1000
	v=d/t
	print 'theta1=',theta1,'theta2=',theta2
	print 'alpha=',alpha,'beta=',beta,'v=',v,'dist=',d
	if alpha > beta:
		
		if theta3 > theta2:
			a=1
			print 'left'
		else:
			a=-1
			print 'right'
		dw=a*(math.radians((alpha-beta)))*v/d
	vr=(2*vb+dw*0.25)/2
	vl=(2*vb-dw*0.25)/2

	vr*=256
	vl*=256
	print 'vr=',vr,'vl=',vl
	return vl,vr
