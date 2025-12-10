"""GTSRB Traffic Sign Classes - German Traffic Sign Recognition Benchmark.

This module contains the 43 traffic sign classes from GTSRB dataset.
Speed limit signs (classes 0-8) are particularly important for ADAS.
"""

# All 43 GTSRB traffic sign classes
GTSRB_CLASSES = {
    0: "speed_limit_20",
    1: "speed_limit_30",
    2: "speed_limit_50",
    3: "speed_limit_60",
    4: "speed_limit_70",
    5: "speed_limit_80",
    6: "end_speed_limit_80",
    7: "speed_limit_100",
    8: "speed_limit_120",
    9: "no_passing",
    10: "no_passing_vehicles_over_3.5t",
    11: "right_of_way_next_intersection",
    12: "priority_road",
    13: "yield",
    14: "stop",
    15: "no_vehicles",
    16: "vehicles_over_3.5t_prohibited",
    17: "no_entry",
    18: "general_caution",
    19: "dangerous_curve_left",
    20: "dangerous_curve_right",
    21: "double_curve",
    22: "bumpy_road",
    23: "slippery_road",
    24: "road_narrows_right",
    25: "road_work",
    26: "traffic_signals",
    27: "pedestrians",
    28: "children_crossing",
    29: "bicycles_crossing",
    30: "beware_ice_snow",
    31: "wild_animals_crossing",
    32: "end_all_limits",
    33: "turn_right_ahead",
    34: "turn_left_ahead",
    35: "ahead_only",
    36: "go_straight_or_right",
    37: "go_straight_or_left",
    38: "keep_right",
    39: "keep_left",
    40: "roundabout_mandatory",
    41: "end_no_passing",
    42: "end_no_passing_vehicles_over_3.5t",
}

# Speed limit classes with their corresponding km/h values
SPEED_LIMIT_CLASSES = {
    0: 20,   # Speed limit 20 km/h
    1: 30,   # Speed limit 30 km/h
    2: 50,   # Speed limit 50 km/h
    3: 60,   # Speed limit 60 km/h
    4: 70,   # Speed limit 70 km/h
    5: 80,   # Speed limit 80 km/h
    6: None, # End of speed limit 80 (use default)
    7: 100,  # Speed limit 100 km/h
    8: 120,  # Speed limit 120 km/h
    32: None,  # End all speed/passing limits
}

# Warning signs that should trigger alerts
WARNING_CLASSES = {
    13: "yield",
    14: "stop",
    17: "no_entry",
    18: "general_caution",
    19: "dangerous_curve_left",
    20: "dangerous_curve_right",
    21: "double_curve",
    22: "bumpy_road",
    23: "slippery_road",
    25: "road_work",
    26: "traffic_signals",
    27: "pedestrians",
    28: "children_crossing",
    29: "bicycles_crossing",
    30: "beware_ice_snow",
    31: "wild_animals_crossing",
}


def get_speed_limit_value(class_id: int) -> int | None:
    """Get the speed limit value in km/h for a given class ID.
    
    Args:
        class_id: GTSRB class ID (0-42)
        
    Returns:
        Speed limit in km/h, or None if not a speed limit sign
    """
    return SPEED_LIMIT_CLASSES.get(class_id)


def get_class_name(class_id: int) -> str:
    """Get the human-readable name for a traffic sign class.
    
    Args:
        class_id: GTSRB class ID (0-42)
        
    Returns:
        Class name as a string
    """
    return GTSRB_CLASSES.get(class_id, f"unknown_{class_id}")


def is_warning_sign(class_id: int) -> bool:
    """Check if a class ID represents a warning sign that should trigger alerts.
    
    Args:
        class_id: GTSRB class ID (0-42)
        
    Returns:
        True if this is a warning sign
    """
    return class_id in WARNING_CLASSES


def is_speed_limit_sign(class_id: int) -> bool:
    """Check if a class ID represents a speed limit sign.
    
    Args:
        class_id: GTSRB class ID (0-42)
        
    Returns:
        True if this is a speed limit sign
    """
    return class_id in SPEED_LIMIT_CLASSES
