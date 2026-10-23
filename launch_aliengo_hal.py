import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../")
os.chdir(dir_path)

import shutil

unitree_legged_sdk_path = dir_path + "/unitree_legged_sdk"
ros2_ws_path = dir_path + "/ros2_ws"


# Ask if we want to delete the old builds and rebuild everything
if os.path.exists(unitree_legged_sdk_path + "/build"):
    answer = input("unitree_legged_sdk is already built. Do you want to delete it and rebuild? [y/N] ")
    if answer.strip().lower() in ["y", "yes"]:
        print("Deleting build folder of unitree_legged_sdk..")
        shutil.rmtree(unitree_legged_sdk_path + "/build", ignore_errors=True)

if os.path.exists(ros2_ws_path + "/build"):
    answer = input("ros2_ws is already built. Do you want to delete it and rebuild? [y/N] ")
    if answer.strip().lower() in ["y", "yes"]:
        print("Deleting build, install and log folders of ros2_ws..")
        shutil.rmtree(ros2_ws_path + "/build", ignore_errors=True)
        shutil.rmtree(ros2_ws_path + "/install", ignore_errors=True)
        shutil.rmtree(ros2_ws_path + "/log", ignore_errors=True)


# Build the unitree legged sdk with the conda compilers, only if needed.
# The last three flags make it work with cmake 4 and find the conda lcm (liblcm-devel: $CONDA_PREFIX/include/lcm, $CONDA_PREFIX/lib/liblcm.so).
# Do not point it to /usr/include or /usr/lib: the system glibc does not match the conda compilers
if not os.path.exists(unitree_legged_sdk_path + "/build/example_torque_aliengo"):
    print("Building unitree_legged_sdk first..")
    os.system("bash -c 'cd unitree_legged_sdk && cmake -S . -B build "
              "-DCMAKE_C_COMPILER=$CONDA_PREFIX/bin/$(uname -m)-conda-linux-gnu-cc "
              "-DCMAKE_CXX_COMPILER=$CONDA_PREFIX/bin/$(uname -m)-conda-linux-gnu-c++ "
              "-DCMAKE_POLICY_VERSION_MINIMUM=3.5 "
              "-DCMAKE_CXX_STANDARD_INCLUDE_DIRECTORIES=$CONDA_PREFIX/include "
              "\"-DCMAKE_EXE_LINKER_FLAGS=-L$CONDA_PREFIX/lib -Wl,-rpath,$CONDA_PREFIX/lib\" "
              "&& cmake --build build'")

# Build the dls2 msgs and the aliengo HAL, only if needed.
# The empty --packages-skip overrides the aliengo_hal skip in ros2_ws/colcon_defaults.yaml
if not os.path.exists(ros2_ws_path + "/install/dls2_interface") or not os.path.exists(ros2_ws_path + "/install/aliengo_hal"):
    print("Building dls2_interface and aliengo_hal first..")
    os.system("bash -c 'cd ros2_ws && colcon build --packages-select dls2_interface aliengo_hal --packages-skip'")


# Run the aliengo HAL
os.system("bash -c 'source unitree_ros2_connect.bash && source ros2_ws/install/setup.bash && ./ros2_ws/install/aliengo_hal/bin/aliengo_hal'")
