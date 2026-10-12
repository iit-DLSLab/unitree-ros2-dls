import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../")
os.chdir(dir_path)

import shutil

cyclonedds_ws_path = dir_path + "/unitree_ros2/cyclonedds_ws"
ros2_ws_path = dir_path + "/ros2_ws"


# Ask if we want to delete the old builds and rebuild everything
if os.path.exists(cyclonedds_ws_path + "/build"):
    answer = input("unitree_ros2/cyclonedds_ws is already built. Do you want to delete it and rebuild? [y/N] ")
    if answer.strip().lower() in ["y", "yes"]:
        print("Deleting build, install and log folders of unitree_ros2/cyclonedds_ws..")
        shutil.rmtree(cyclonedds_ws_path + "/build", ignore_errors=True)
        shutil.rmtree(cyclonedds_ws_path + "/install", ignore_errors=True)
        shutil.rmtree(cyclonedds_ws_path + "/log", ignore_errors=True)

if os.path.exists(ros2_ws_path + "/build"):
    answer = input("ros2_ws is already built. Do you want to delete it and rebuild? [y/N] ")
    if answer.strip().lower() in ["y", "yes"]:
        print("Deleting build, install and log folders of ros2_ws..")
        shutil.rmtree(ros2_ws_path + "/build", ignore_errors=True)
        shutil.rmtree(ros2_ws_path + "/install", ignore_errors=True)
        shutil.rmtree(ros2_ws_path + "/log", ignore_errors=True)


# Build the unitree msgs, only if needed
if not os.path.exists(cyclonedds_ws_path + "/install"):
    print("Building unitree_ros2/cyclonedds_ws first..")
    os.system("bash -c 'cd unitree_ros2/cyclonedds_ws && colcon build'")

# Build the dls2 msgs, the go2 HAL and the a2 HAL, only if needed
if not os.path.exists(ros2_ws_path + "/install/dls2_interface") or not os.path.exists(ros2_ws_path + "/install/go2_hal") or not os.path.exists(ros2_ws_path + "/install/a2_hal"):
    print("Building dls2_interface, go2_hal and a2_hal first..")
    os.system("bash -c 'source unitree_ros2/cyclonedds_ws/install/setup.bash && cd ros2_ws && colcon build --packages-select dls2_interface go2_hal a2_hal'")


# Run the go2 HAL
os.system("bash -c 'source unitree_ros2/cyclonedds_ws/install/setup.bash && source unitree_ros2_connect.bash && source ros2_ws/install/setup.bash && ./ros2_ws/install/go2_hal/bin/go2_hal'")
