import numpy as np
from scipy.stats import zscore

# generate surrogate signals for surrogate-driven and surrogate-optimized method
rpm = np.loadtxt("./data/rpm_signal.txt")
rpm_grad = np.gradient(rpm)
np.savetxt("./data/surrogate_rpm_grad.txt",np.stack([zscore(rpm),zscore(rpm_grad)],axis=-1),fmt="%f")

# generate phase-drived sinusoidal surrogate signals for surrogate-free method
timeIndicesPerSliceAndPhase=np.loadtxt(f"./data/timeIndicesPerSliceAndPhase.txt",dtype=int)
phases=np.array([np.where(timeIndicesPerSliceAndPhase==i)[1][0] for i in range(rpm.shape[0])])
phaseSignalInterp=lambda phase: np.array([np.sin(2*np.pi*phase/10),np.cos(2*np.pi*phase/10)])
surr_phase=phaseSignalInterp(phases)
np.savetxt(f"./data/surrogate_phase_derived.txt",surr_phase.T,fmt="%f")