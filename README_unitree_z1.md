## Install Z1 sdk and controller packages

First, initialise the submodules (required before any cmake step):

```bash
git submodule update --init --recursive
```

### Easiest: compile with the launchers

From the repository root, with your conda/pixi environment activated:

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

## Running the Z1 HAL

**(TERMINAL 1)** From the repo root, start the Z1 controller:

```bash
python3 launch_z1_controller.py
```

**(TERMINAL 2)** From the repo root, start the HAL node:

```bash
python3 launch_z1_hal.py
```
