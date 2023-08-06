import numpy as np
import matplotlib.pyplot as plt
import healpy as hp
import pymaster as nmt
from scipy.linalg import toeplitz

nside = 256
msk = hp.ud_grade(hp.read_map("../sandbox_validation/data/mask_lss.fits", verbose=False), nside_out=nside)
mp = np.random.randn(len(msk))

b = nmt.NmtBin(nside, nlb=4)
f = nmt.NmtField(msk, [mp])
print("Workspacing")
w = nmt.NmtWorkspace()
w.compute_coupling_matrix(f, f, b)
print("Workspacing")
wt = nmt.NmtWorkspace()
l_toeplitz = int(1.5*nside)
l_exact = nside // 2
dl_band = 30
wt.compute_coupling_matrix(f, f, b, l_toeplitz=l_toeplitz, l_exact=l_exact, dl_band=dl_band)

ls = np.arange(3*nside, dtype=int)

c = w.get_coupling_matrix() / (2*ls[None, :]+1.)
ct = wt.get_coupling_matrix() / (2*ls[None, :]+1.)

r = c / np.sqrt(np.diag(c)[:, None]*
                np.diag(c)[None, :])
col = r[:, l_toeplitz]
col0 = col[(np.arange(3*nside)+l_toeplitz) % (3*nside)]

rb = toeplitz(col0)
cb = rb*np.sqrt(np.diag(c)[:, None]*np.diag(c)[None, :])

plt.figure()
plt.plot(np.diag(c), 'k-')
plt.plot(np.diag(ct), 'r-')
plt.plot(np.diag(cb), 'b--')

plt.figure()
plt.imshow(np.log10(np.fabs(c)), interpolation='nearest')
plt.colorbar()
plt.figure()
plt.imshow(np.log10(np.fabs(ct)), interpolation='nearest')
plt.colorbar()
plt.figure()
plt.imshow(np.log10(np.fabs(cb)), interpolation='nearest')
plt.colorbar()
plt.figure()
plt.imshow(ct-cb, interpolation='nearest')
plt.colorbar()
plt.figure()
plt.imshow(ct-c, interpolation='nearest')
plt.colorbar()

plt.figure()
plt.plot(col, 'k-')
plt.plot(col0, 'r-')
plt.show()
