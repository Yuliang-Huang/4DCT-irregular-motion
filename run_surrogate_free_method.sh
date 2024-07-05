echo "Running the surrogate-free method"

datadir=./data/
refStateImg=${datadir}/ref_empty_image.nii.gz
numberOfTimepoints=182
dynImgTxtFile=${datadir}/dynamic_image_files.txt
numberOfSurrogates=2
surrTxtFile=${datadir}/surrogate_phase_derived.txt
outputdir=output/surr_free/
mkdir -p ${outputdir}

echo "fitting the motion model and reconstructing the motion-compensated image..."

./runSupremo -dType 1 -mcrType 3 -optimiserType 2 -maxFitIt 5 -maxSwitchIt 6 -lr 0.01 -nThreads 8 \
 -refState ${refStateImg} -dynamic ${numberOfTimepoints} ${dynImgTxtFile} -surr ${numberOfSurrogates} ${surrTxtFile} -sx -5 -sy -5 -sz -5 -ln 3 -lp 3 -sim SSD -be 0.0 \
 -outMCR ${outputdir}/finalImage.nii.gz -outRCM ${outputdir}/motionModel.nii.gz -outSurr ${outputdir}/outSurr.txt | tee ${outputdir}/log.txt
echo "log file is saved in ${outputdir}/log.txt"
echo "motion compensated image is saved in ${outputdir}/finalImage.nii.gz"
echo "motion model is saved in ${outputdir}/motionModel_t00.nii.gz"

echo "animating the reconstructed motion-compensated image by the motion model..." 

mkdir -p ${outputdir}/estimated_volumes/
./animate 8 ${outputdir}/outSurr.txt ${numberOfSurrogates} ${outputdir}/motionModel_t00.nii.gz  3 ${outputdir}/finalImage.nii.gz ${refStateImg} ${outputdir}/estimated_volumes/ 
echo "The output volumes for each time point are saved in ${outputdir}/estimated_volumes/" 

echo "estimating the tumor masks for each time point..."
mkdir -p ${outputdir}/estimated_tumormasks/
./animate 8 ${outputdir}/outSurr.txt ${numberOfSurrogates} ${outputdir}/motionModel_t00.nii.gz  3 ${datadir}/ref_tumormask.nii.gz  ${refStateImg} ${outputdir}/estimated_tumormasks/
echo "The output tumor masks for each time point are saved in ${outputdir}/estimated_tumormasks/"