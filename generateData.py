import numpy as np
import nibabel as nib
from tqdm import tqdm
from glob import glob
import os
import nibabel as nib

datadir="./data/"

gtVolumeNames=glob(f"{datadir}/ground_truth/volumes/*.nii.gz")
gtVolumeNames.sort(key=lambda name: int(name.split("_")[-1].split(".")[0]))

# load the index of time point when each slice of each phase is acquired
# dimension: (num_slices, num_phases), start from the bottom slice and the peak inhale phase
timeIndicesPerSliceAndPhase=np.loadtxt(f"{datadir}/timeIndicesPerSliceAndPhase.txt",dtype=int)

# fetch the slices taken at each couch position
os.makedirs(f"{datadir}/unsort_ct_slabs",exist_ok=True)
print("saving unsort CT slabs...")
for i in tqdm(range(len(gtVolumeNames))):
    activeSlices = np.nonzero(timeIndicesPerSliceAndPhase==i)[0]
    volume = nib.load(gtVolumeNames[i])
    affine = volume.affine
    affine[:,-1] = np.dot(affine,np.array([0,0,np.min(activeSlices),1]))
    nib.nifti1.save(nib.Nifti1Image(volume.get_fdata()[:,:,activeSlices].astype(np.float32),affine),f"{datadir}/unsort_ct_slabs/slab_{i}.nii.gz")

# create a text file to store the path of each CT slab
with open(f"{datadir}/dynamic_image_files.txt","w") as f:
    for i in range(len(gtVolumeNames)):
        f.write(f"{datadir}/unsort_ct_slabs/slab_{i}.nii.gz\n")
    f.flush()
    f.close()

# sort the slabs into ten phases
print("saving sorted 4DCT...")
os.makedirs(f"{datadir}/sorted_4dct",exist_ok=True)
affine=nib.load(gtVolumeNames[0]).affine
for i in tqdm(range(10)):
    time_points_to_include = np.unique(timeIndicesPerSliceAndPhase[:,i])
    sorted_volumes = [nib.load(f"{datadir}/unsort_ct_slabs/slab_{t}.nii.gz").get_fdata().astype(np.float32) for t in time_points_to_include[::-1]]
    nib.nifti1.save(nib.Nifti1Image(np.concatenate(sorted_volumes,axis=-1),affine),f"{datadir}/sorted_4dct/phase_{i}.nii.gz")