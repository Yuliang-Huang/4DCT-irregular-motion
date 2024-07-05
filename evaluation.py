import numpy as np
import nibabel as nib
from glob import glob
from tqdm import tqdm
from skimage.measure import regionprops,label
from argparse import ArgumentParser


def main(args):
    print("Evaluating the performance of the estimated volumes and masks...")
    if args.dir_gtVolume is None:
        raise ValueError("Please provide the path to the ground truth volumes")
    gtVolumeNames=glob(f"{args.dir_gtVolume}/*.nii.gz")
    gtVolumeNames.sort(key=lambda name: int(name.split("_")[-1].split(".")[0]))
    
    if args.dir_gtMask is None:
        raise ValueError("Please provide the path to the ground truth masks")
    gtMaskNames=glob(f"{args.dir_gtMask}/*.nii.gz")
    gtMaskNames.sort(key=lambda name: int(name.split("_")[-1].split(".")[0]))

    if args.dir_estimatedVolume is None:
        raise ValueError("Please provide the path to the estimated volumes")
    estimatedVolumeNames=glob(f"{args.dir_estimatedVolume}/*.nii.gz")
    estimatedVolumeNames.sort(key=lambda name: int(name.split("_")[-1].split(".")[0]))

    if args.dir_estimatedMask is None:
        raise ValueError("Please provide the path to the estimated masks")
    estimatedMaskNames=glob(f"{args.dir_estimatedMask}/*.nii.gz")
    estimatedMaskNames.sort(key=lambda name: int(name.split("_")[-1].split(".")[0]))

    mse=[]
    dice=[]
    centroid=np.zeros((len(gtVolumeNames),2,3))
    print(f"reading files from {args.dir_estimatedVolume} and {args.dir_estimatedMask}")
    print("Calculating the Mean Squared Error and Dice Coefficient...")
    for i in tqdm(range(len(gtVolumeNames))):
        gtVolume=nib.load(gtVolumeNames[i]).get_fdata()
        gtMask=nib.load(gtMaskNames[i]).get_fdata()
        estimatedVolume=nib.load(estimatedVolumeNames[i]).get_fdata()
        estimatedMask=nib.load(estimatedMaskNames[i]).get_fdata()>0.5
        mse.append(np.nanmean(np.square(gtVolume-estimatedVolume)))
        dice.append(2*np.sum(gtMask*estimatedMask)/(np.sum(gtMask)+np.sum(estimatedMask)))
        centroid[i,0]=np.array(regionprops(label(gtMask))[0].centroid)
        centroid[i,1]=np.array(regionprops(label(estimatedMask))[0].centroid)

    print(f"Mean Squared Error: {np.mean(np.sqrt(mse))}")
    print(f"Dice Coefficient: {np.mean(dice)}")
    gap=np.sqrt(np.sum(np.square(np.array(centroid[:,1])-np.array(centroid[:,0])),axis=-1))
    print(f"Mean gap between centroids: {np.mean(gap)}")

if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--dir_gtVolume", type=str, default=None)
    arg_parser.add_argument("--dir_estimatedVolume", type=str, default=None)
    arg_parser.add_argument("--dir_gtMask", type=str, default=None)
    arg_parser.add_argument("--dir_estimatedMask", type=str, default=None)
    args = arg_parser.parse_args()
    main(args)