import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../")
os.chdir(dir_path)

import shutil

z1_controller_path = dir_path + "/unitree_z1/z1_controller"
z1_sdk_path = dir_path + "/unitree_z1/z1_sdk"


# Ask if we want to delete the old builds and rebuild everything
if os.path.exists(z1_controller_path + "/build"):
    answer = input("unitree_z1/z1_controller is already built. Do you want to delete it and rebuild? [y/N] ")
    if answer.strip().lower() in ["y", "yes"]:
        print("Deleting build folder of unitree_z1/z1_controller..")
        shutil.rmtree(z1_controller_path + "/build", ignore_errors=True)

if os.path.exists(z1_sdk_path + "/build"):
    answer = input("unitree_z1/z1_sdk is already built. Do you want to delete it and rebuild? [y/N] ")
    if answer.strip().lower() in ["y", "yes"]:
        print("Deleting build folder of unitree_z1/z1_sdk..")
        shutil.rmtree(z1_sdk_path + "/build", ignore_errors=True)


# Build the z1 controller, only if needed
if not os.path.exists(z1_controller_path + "/build/z1_ctrl"):
    print("Building unitree_z1/z1_controller first..")
    os.system("bash -c 'cd unitree_z1/z1_controller && mkdir -p build && cd build && cmake -DCMAKE_POLICY_VERSION_MINIMUM=3.5 .. && make -j4'")

# Build the z1 sdk, only if needed. This also builds its python interface (unitree_z1/z1_sdk/lib) used by the z1 HAL
if not os.path.exists(z1_sdk_path + "/build/highcmd_basic"):
    print("Building unitree_z1/z1_sdk first..")
    os.system("bash -c 'cd unitree_z1/z1_sdk && mkdir -p build && cd build && cmake -DCMAKE_POLICY_VERSION_MINIMUM=3.5 .. && make -j4'")


# Run the z1 controller
os.system("bash -c 'cd unitree_z1/z1_controller/build && ./z1_ctrl'")
