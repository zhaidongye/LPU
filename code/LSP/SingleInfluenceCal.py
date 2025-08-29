import numpy as np
def SingleInfluCal(point, candidate_point, point_next_direction, alpha):

    distance = np.linalg.norm(np.array(point) - np.array(candidate_point))
    if distance == 0:
        return np.array([0.0, 0.0])  

    influence_strength = distance ** (-alpha)
    
    direction_vector = np.array(candidate_point) - np.array(point)
    point_next_direction = np.array(point_next_direction)
    if np.linalg.norm(point_next_direction) == 0:
        combined_direction = direction_vector / np.linalg.norm(direction_vector)
    else:
        point_next_direction_unit = point_next_direction / np.linalg.norm(point_next_direction)
        projection_length = np.dot(direction_vector, point_next_direction_unit)
        combined_direction = projection_length * point_next_direction_unit
    
        combined_direction = combined_direction / np.linalg.norm(combined_direction) if np.linalg.norm(combined_direction) != 0 else combined_direction
    
    influence_vector = influence_strength * combined_direction

    return influence_vector