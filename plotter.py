import matplotlib.pyplot as plt
from itertools import cycle

def plot(C):
	plt.figure(1)
	plt.clf()
	plt.axis([-2000,2000,0,2000])
	colors = plt.cm.Spectral(np.linspace(0, 1, len(C)))
	
	for k, col in zip(C, colors):
	    plt.plot(C[k]['cords'][:,0], C[k]['cords'][:,1], 'o', markerfacecolor=col,markeredgecolor='k',markersize=5)
	    plt.plot(C[k]['center'][0],C[k]['center'][1], 'o', markerfacecolor=col,markeredgecolor='k', markersize=14)
	
	plt.title('Estimated number of clusters: %d' % n_clusters_)
	plt.show()