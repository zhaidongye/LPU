from LSP.SinglePointPerturb import SingePerturb
import numpy as np
def TrajectoryPerturb(trajectory,nodes_within_radius,alpha):
    TrajectoryPerturbed = np.zeros_like(trajectory)
    for i in range(len(trajectory)):
        point_next_direction = np.array(trajectory[i+1]) - np.array(trajectory[i]) if i < len(trajectory)-1 else np.array([0.0, 0.0])
        TrajectoryPerturbed.iloc[i] = SingePerturb(trajectory[i],nodes_within_radius,point_next_direction,alpha)
    return TrajectoryPerturbed