## Install LCM (required)

The Unitree Legged SDK and `aliengo_hal` need LCM installed on the system:

```bash
sudo apt install liblcm-dev
```

## Compile the Unitree Legged SDK and the Aliengo HAL

### Easiest: compile with the launcher

From the repository root, with your conda/pixi environment activated, just run:

```bash
python3 launch_aliengo_hal.py
```

The first time, the launcher compiles everything Aliengo needs (the Unitree Legged SDK, and the ROS 2 packages `dls2_interface` and `aliengo_hal`) and then starts the HAL. The next times it only starts the HAL. If a build folder already exists, it first asks whether to delete it and rebuild from scratch.

### What the launcher does, by hand

From the repository root, with your conda/pixi environment activated:

1. Compile the Unitree Legged SDK (the launcher does it only if `unitree_legged_sdk/build/example_torque_aliengo` does not exist):

```bash
cd unitree_legged_sdk
cmake -S . -B build \
  -DCMAKE_C_COMPILER=$CONDA_PREFIX/bin/$(uname -m)-conda-linux-gnu-cc \
  -DCMAKE_CXX_COMPILER=$CONDA_PREFIX/bin/$(uname -m)-conda-linux-gnu-c++ \
  -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
  -DCMAKE_CXX_STANDARD_INCLUDE_DIRECTORIES=/usr/include \
  -DCMAKE_EXE_LINKER_FLAGS=-L/usr/lib/$(uname -m)-linux-gnu
cmake --build build
cd ..
```

The last three flags let cmake 4 configure the SDK and let the conda compilers find the system LCM, so the CMakeLists.txt of **unitree_legged_sdk** does not need to be modified. There is no install step.

2. Compile the DLS2 messages and the Aliengo HAL in **ros2_ws** (the launcher does it only if `ros2_ws/install/dls2_interface` or `ros2_ws/install/aliengo_hal` do not exist):

```bash
cd ros2_ws
colcon build --packages-select dls2_interface aliengo_hal --packages-skip
cd ..
```

`aliengo_hal` is excluded from a plain `colcon build` by
[ros2_ws/colcon_defaults.yaml](./ros2_ws/colcon_defaults.yaml) while its fix is pending:

```yaml
build:
  packages-skip:
    - aliengo_hal
```

The empty `--packages-skip` overrides this exclusion. Selecting Aliengo alone does not override it.

3. Start the HAL:

```bash
source unitree_ros2_connect.bash
source ros2_ws/install/setup.bash
./ros2_ws/install/aliengo_hal/bin/aliengo_hal
```

To rebuild from scratch, delete the build folders first (this is what answering `y` to the launcher does):

```bash
rm -rf unitree_legged_sdk/build
rm -rf ros2_ws/build ros2_ws/install ros2_ws/log
```

## Running the aliengo hal
Open a terminal and input:
```bash
unitree_ros2_connect
```
**Note that in every terminal where you launch your other scripts, you need to source this file first. Put it in .bashrc as an alias!**

Then run in the terminal:
```bash
python3 launch_aliengo_hal.py
```
