

from .inspire_dds import inspire_hand_touch,inspire_hand_ctrl,inspire_hand_state
import threading
modbus_lock = threading.Lock()

# Data definitions   
data_sheet = [
    ("Little Finger Tip Touch Data", 3000, 18, (3, 3), "fingerone_tip_touch"),      # Little finger tip touch data
    ("Little Finger Top Touch Data", 3018, 192, (12, 8), "fingerone_top_touch"),      # Little finger top touch data
    ("Little Finger Palm Touch Data", 3210, 160, (10, 8), "fingerone_palm_touch"),     # Little finger palm touch data
    ("Ring Finger Tip Touch Data", 3370, 18, (3, 3), "fingertwo_tip_touch"),      # Ring finger tip touch data
    ("Ring Finger Top Touch Data", 3388, 192, (12, 8), "fingertwo_top_touch"),      # Ring finger top touch data
    ("Ring Finger Palm Touch Data", 3580, 160, (10, 8), "fingertwo_palm_touch"),     # Ring finger palm touch data
    ("Middle Finger Tip Touch Data", 3740, 18, (3, 3), "fingerthree_tip_touch"),    # Middle finger tip touch data
    ("Middle Finger Top Touch Data", 3758, 192, (12, 8), "fingerthree_top_touch"),    # Middle finger top touch data
    ("Middle Finger Palm Touch Data", 3950, 160, (10, 8), "fingerthree_palm_touch"),   # Middle finger palm touch data
    ("Index Finger Tip Touch Data", 4110, 18, (3, 3), "fingerfour_tip_touch"),     # Index finger tip touch data
    ("Index Finger Top Touch Data", 4128, 192, (12, 8), "fingerfour_top_touch"),     # Index finger top touch data
    ("Index Finger Palm Touch Data", 4320, 160, (10, 8), "fingerfour_palm_touch"),    # Index finger palm touch data
    ("Thumb Tip Touch Data", 4480, 18, (3, 3), "fingerfive_tip_touch"),     # Thumb tip touch data
    ("Thumb Top Touch Data", 4498, 192, (12, 8), "fingerfive_top_touch"),     # Thumb top touch data
    ("Thumb Middle Touch Data", 4690, 18, (3, 3), "fingerfive_middle_touch"),  # Thumb middle touch data
    ("Thumb Palm Touch Data", 4708, 192, (12, 8), "fingerfive_palm_touch"),    # Thumb palm touch data
    ("Palm Touch Data", 4900, 224, (14, 8), "palm_touch")                # Palm touch data
]

status_codes = {
    0: "Releasing",
    1: "Grabbing",
    2: "Position Reached, Stopped",
    3: "Force Control Reached, Stopped",
    5: "Current Protection Stopped",
    6: "Electric Cylinder Stalling Stopped",
    7: "Electric Cylinder Fault Stopped",
    255: "Error"
}

error_descriptions = {
    0: "Stalling Fault",
    1: "Overtemperature Fault",
    2: "Overcurrent Fault",
    3: "Motor Abnormality",
    4: "Communication Fault"
}

def get_error_description(error_value):
    error_reasons = []
    # Check each bit to see if it's set to 1, if so, add the corresponding fault description
    for bit, description in error_descriptions.items():
        if error_value & (1 << bit):  # Use bitwise operation to check if the corresponding bit is 1
            error_reasons.append(description)
    return error_reasons

# Print a summary of all error reasons
def update_error_label(ERROR):
    error_summary = []
    for e in ERROR:
        binary_error = '{:04b}'.format(int(e))  # Convert to 4-bit binary representation
        error_reasons = get_error_description(int(e))  # Get list of error reasons
        if error_reasons:
            error_summary.append(f"ERROR {e} ({binary_error}): " + ', '.join(error_reasons))
        else:
            error_summary.append(f"ERROR {e} ({binary_error}): No fault")
    # Update label content
    # print("\n".join(error_summary))
    return "\t".join(error_summary)


def get_inspire_hand_touch():
    return inspire_hand_touch(
        fingerone_tip_touch=[0 for _ in range(9)],        # Little finger tip touch data
        fingerone_top_touch=[0 for _ in range(96)],       # Little finger top touch data
        fingerone_palm_touch=[0 for _ in range(80)],      # Little finger palm touch data
        fingertwo_tip_touch=[0 for _ in range(9)],        # Ring finger tip touch data
        fingertwo_top_touch=[0 for _ in range(96)],       # Ring finger top touch data
        fingertwo_palm_touch=[0 for _ in range(80)],      # Ring finger palm touch data
        fingerthree_tip_touch=[0 for _ in range(9)],      # Middle finger tip touch data
        fingerthree_top_touch=[0 for _ in range(96)],     # Middle finger top touch data
        fingerthree_palm_touch=[0 for _ in range(80)],    # Middle finger palm touch data
        fingerfour_tip_touch=[0 for _ in range(9)],       # Index finger tip touch data
        fingerfour_top_touch=[0 for _ in range(96)],      # Index finger top touch data
        fingerfour_palm_touch=[0 for _ in range(80)],     # Index finger palm touch data
        fingerfive_tip_touch=[0 for _ in range(9)],       # Thumb tip touch data
        fingerfive_top_touch=[0 for _ in range(96)],      # Thumb top touch data
        fingerfive_middle_touch=[0 for _ in range(9)],    # Thumb middle touch data
        fingerfive_palm_touch=[0 for _ in range(96)],     # Thumb palm touch data
        palm_touch=[0 for _ in range(112)]                # Palm touch data
    )
    
def get_inspire_hand_state():
    return inspire_hand_state(
        pos_act=[0 for _ in range(6)],        # Position actuators
        angle_act=[0 for _ in range(6)],       # Angle actuators
        force_act=[0 for _ in range(6)],      # Force actuators
        current=[0 for _ in range(6)],        # Current sensors
        err=[0 for _ in range(6)],            # Error codes
        status=[0 for _ in range(6)],         # Status codes
        temperature=[0 for _ in range(6)],    # Temperature sensors
    ) 

def get_inspire_hand_ctrl():
    return inspire_hand_ctrl(
        pos_set=[0 for _ in range(6)],        # Position set values
        angle_set=[0 for _ in range(6)],       # Angle set values
        force_set=[0 for _ in range(6)],      # Force set values
        speed_set=[0 for _ in range(6)],      # Speed set values
        mode=0b0000  # Mode set to all zeros (no operation)
    ) 

defaut_ip = '192.168.11.210'  # Default IP address
