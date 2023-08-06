from histmp import histogram
import numpy as np

nbins = 12
xmin = -3
xmax = 3

x = np.random.randn(1000000).astype(np.float32)
w = np.random.uniform(.5, .6, x.shape[0])

res = histogram(x, weights=w, bins=nbins, range=(xmin, xmax), flow=False, density=True)
nh = np.histogram(x, bins=nbins, range=(xmin, xmax), weights=w, density=True)

underf = np.sum(w[x<xmin])
overf = np.sum(w[x>xmax])

print(underf)
print(overf)

print(res[0])
print("--")
print(nh[0])


print(np.allclose(res[0], nh[0]))
#print(nh[0][0] + underf)
#print(nh[0][-1] + overf)
