from matplotlib import pyplot as plt
import matplotlib.animation as animation
import numpy as np
import nibabel as nib
from scipy.signal import find_peaks

from glob import glob

datadir="./data/"
yslice=179
first_n_timepoints=50

timeIndicesPerSliceAndPhase=np.loadtxt(f"./data/timeIndicesPerSliceAndPhase.txt",dtype=int)
rpm_signal = np.loadtxt(f"{datadir}/rpm_signal.txt",dtype=float)

gtVolumeNames=glob(f"{datadir}/ground_truth/volumes/*.nii.gz")
gtVolumeNames.sort(key=lambda name: int(name.split("_")[-1].split(".")[0]))
gtVolumes = [nib.load(name).get_fdata()[:,yslice].T for name in gtVolumeNames[:first_n_timepoints]]

unsortSlabNames=np.loadtxt(f"{datadir}/dynamic_image_files.txt",dtype=str)
unsort_slabs = [nib.load(name).get_fdata()[:,yslice].T for name in unsortSlabNames[:first_n_timepoints]]

sorted4DCTNames=glob(f"{datadir}/sorted_4dct/*.nii.gz")
sorted4DCTs = [nib.load(name).get_fdata()[:,yslice].T for name in sorted4DCTNames]

activePhases = [np.where(timeIndicesPerSliceAndPhase==t)[1][0] for t in range(rpm_signal.shape[0])]

fontsize=20
fig = plt.figure(figsize=(15,6))
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
ax1,ax2,ax3 = fig.subplots(1,3)
im1=ax1.imshow(sorted4DCTs[activePhases[0]],'gray',aspect=3,origin='lower')
ax1.axis('off');
ax1.set_title(f"4DCT Phase{activePhases[0]*10}%",fontsize=fontsize)
tmp = -1000*np.ones_like(sorted4DCTs[0])
tmp[timeIndicesPerSliceAndPhase[:,activePhases[0]]==0] = unsort_slabs[0]
im2=ax2.imshow(tmp,'gray',aspect=3,origin='lower')
ax2.axis('off')
ax2.set_title(f"Slab at t={0}",fontsize=fontsize)
im3=ax3.imshow(gtVolumes[0],'gray',aspect=3,origin='lower')
ax3.axis('off')
ax3.set_title(f"GT Volume at t={0}",fontsize=fontsize)
plt.tight_layout()

def animate_func(i):
    im1.set_array(sorted4DCTs[activePhases[i]])
    ax1.set_title(f"4DCT Phase{activePhases[i]*10}%",fontsize=fontsize)
    tmp = -1000*np.ones_like(sorted4DCTs[0])
    tmp[timeIndicesPerSliceAndPhase[:,activePhases[i]]==i] = unsort_slabs[i]
    im2.set_array(tmp)
    ax2.set_title(f"Slab at t={i}",fontsize=fontsize)
    im3.set_array(gtVolumes[i])
    ax3.set_title(f"GT Volume at t={i}",fontsize=fontsize)
    return im1,im2,im3

fps=10
anim = animation.FuncAnimation(
                               fig,
                               animate_func,
                               frames = len(gtVolumes),
                               interval = 1000 / fps, # in ms
                               )
Writer = animation.writers['pillow']
writer = Writer(fps=10, bitrate=900) #<-- increase bitrate
anim.save(f"phantom_animation.gif", writer=writer,dpi=100)