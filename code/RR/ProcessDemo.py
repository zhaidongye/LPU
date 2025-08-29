import osmnx as ox
import pandas as pd

import os
import glob



north, south = 40.05, 39.8
east, west = 116.55, 116.2


graph_file = "LPU-master/data/RoadNetwork/Beijing_drive_network.graphml"
if os.path.exists(graph_file):
    G = ox.load_graphml(graph_file)
else:
    G = ox.graph_from_bbox(north, south, east, west, network_type='drive')
    
    ox.save_graphml(G, graph_file)



trajectory_dir = "LPU-master/data/TDrive/taxi_log_2008_by_id"
trajectory_files = glob.glob(os.path.join(trajectory_dir, "*.txt"))

selected_trajectory = None
for file in trajectory_files:
    df = pd.read_csv(file, header=None, names=['taxi_id', 'timestamp', 'lon', 'lat'])
    
    centroid_lon = df['lon'].mean()
    centroid_lat = df['lat'].mean()
    if south <= centroid_lat <= north and west <= centroid_lon <= east:
        selected_trajectory = df
        
        break
if selected_trajectory is None:
    raise ValueError("error: No trajectory found within the specified bounding box.")
trajectory = selected_trajectory

trajectory = trajectory[
    (trajectory['lat'] >= south) & (trajectory['lat'] <= north) &
    (trajectory['lon'] >= west) & (trajectory['lon'] <= east)
].reset_index(drop=True)

from RR.RestrictRegion import restric_region

R_max,nodes_within_radius=restric_region(trajectory,G)

