import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../")
os.chdir(dir_path)

import shutil

ros2_ws_path = dir_path + "/ros2_ws"


# Ask if we want to delete the old builds and rebuild everything
if os.path.exists(ros2_ws_path + "/build"):
    answer = input("ros2_ws is already built. Do you want to delete it and rebuild? [y/N] ")
    if answer.strip().lower() in ["y", "yes"]:
        print("Deleting build, install and log folders of ros2_ws..")
        shutil.rmtree(ros2_ws_path + "/build", ignore_errors=True)
        shutil.rmtree(ros2_ws_path + "/install", ignore_errors=True)
        shutil.rmtree(ros2_ws_path + "/log", ignore_errors=True)


# Build the dls2 msgs, only if needed
if not os.path.exists(ros2_ws_path + "/install/dls2_interface"):
    print("Building dls2_interface first..")
    os.system("bash -c 'cd ros2_ws && colcon build --packages-select dls2_interface'")


# Run the z1 HAL
os.system("bash -c 'source ros2_ws/install/setup.bash && python3 ros2_ws/src/z1_hal/z1_hal.py'")
