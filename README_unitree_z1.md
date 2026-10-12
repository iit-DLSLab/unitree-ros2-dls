## Install Z1 sdk and controller packages

First, initialise the submodules (required before any cmake step):

```bash
git submodule update --init --recursive
```

### Easiest: compile with the launchers

From the repository root, with your conda/pixi environment activated (after the [network configuration](#network-configuration)):

- `python3 launch_z1_controller.py` compiles **z1_controller** and **z1_sdk** (with its python interface, used by the Z1 HAL) the first time, and then starts the Z1 controller.
- `python3 launch_z1_hal.py` compiles the DLS2 messages (`dls2_interface` in **ros2_ws**) the first time, and then starts the Z1 HAL.

The next times they only start the controller/HAL. If a build folder already exists, they first ask whether to delete it and rebuild from scratch. Run `launch_z1_controller.py` first (see [Running the Z1 HAL](#running-the-z1-hal)), since the Z1 HAL needs the python interface of **z1_sdk**.

### What the launchers do, by hand

From the repository root, with your conda/pixi environment activated:

1. Compile **z1_controller** (`launch_z1_controller.py` does it only if `unitree_z1/z1_controller/build/z1_ctrl` does not exist):

```bash
cd unitree_z1/z1_controller
mkdir -p build && cd build
cmake -DCMAKE_POLICY_VERSION_MINIMUM=3.5 ..
make -j4
cd ../../..
```

2. Compile **z1_sdk** and its python interface in `unitree_z1/z1_sdk/lib` (`launch_z1_controller.py` does it only if `unitree_z1/z1_sdk/build/highcmd_basic` does not exist):

```bash
cd unitree_z1/z1_sdk
mkdir -p build && cd build
cmake -DCMAKE_POLICY_VERSION_MINIMUM=3.5 ..
make -j4
cd ../../..
```

3. Compile the DLS2 messages in **ros2_ws** (`launch_z1_hal.py` does it only if `ros2_ws/install/dls2_interface` does not exist):

```bash
cd ros2_ws
colcon build --packages-select dls2_interface
cd ..
```

4. Start the controller (`launch_z1_controller.py`) and, in another terminal, the HAL (`launch_z1_hal.py`):

```bash
cd unitree_z1/z1_controller/build && ./z1_ctrl
```

```bash
source ros2_ws/install/setup.bash
python3 ros2_ws/src/z1_hal/z1_hal.py
```

To rebuild from scratch, delete the build folders first (this is what answering `y` to the launchers does):

```bash
rm -rf unitree_z1/z1_controller/build unitree_z1/z1_sdk/build # launch_z1_controller.py
rm -rf ros2_ws/build ros2_ws/install ros2_ws/log             # launch_z1_hal.py
```


## Network configuration

1. Connect the Z1 arm and the computer using an Ethernet cable. Then, open the network settings, find the network interface to which the arm is connected. In IPv4 setting, **change the IPv4 mode to manual, set the address to a free IP of the robot network (e.g. 192.168.123.111), and set the mask to 255.255.255.0**. Do not use 192.168.123.110, which is the Z1 arm (the Z1 controller talks to it via UDP on port 8881, see `unitree_z1/z1_controller/config/config.xml`). If the Z1 is mounted on a quadruped and reachable through the same network, the IP already set for the quadruped works too. After completion, click apply and wait for the network to reconnect.

2. Ensure that the network of the arm is connected correctly by opening a terminal and writing:
```bash
ping 192.168.123.110
```

The Z1 HAL talks only locally with the Z1 controller, so **unitree_ros2_connect.bash** is not needed for the Z1.


## Running the Z1 HAL

**(TERMINAL 1)** From the repo root, start the Z1 controller:

```bash
python3 launch_z1_controller.py
```

**(TERMINAL 2)** From the repo root, start the HAL node:

```bash
python3 launch_z1_hal.py
```
