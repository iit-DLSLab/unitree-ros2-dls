## LCM (required)

The Unitree Legged SDK and `aliengo_hal` need LCM. It comes from the conda/pixi environment (`liblcm-devel` from conda-forge, already listed in [installation/pixi.toml](./installation/pixi.toml) and in the mamba yaml files). If your environment was created before it was added, update it:

```bash
cd installation && pixi install -e humble   # or: mamba install -c conda-forge liblcm-devel
```

Do not use the system LCM (`sudo apt install liblcm-dev`): it is built against the system glibc, which does not match the conda compilers, and linking fails (e.g. `undefined reference to '__libc_csu_init'`).

## Real-time priority (recommended)

When it starts, the HAL locks its memory and switches to real-time scheduling (`SCHED_FIFO`, priority 99), like the SDK `InitEnvironment()`. If your user is not allowed to do this, the HAL prints `Warning: real-time priority not allowed` (or `Warning: mlockall failed`) and keeps running with normal priority, so the 500 Hz loops are less regular. On the real robot, allow it once:

```bash
sudo tee /etc/security/limits.d/99-unitree-realtime.conf <<EOF
$(id -un)  -  rtprio   99
$(id -un)  -  memlock  unlimited
EOF
```

Then log out and log in again (or reboot), and check that `ulimit -r` prints `99`.

To try it right away without logging out, raise the limits of the current terminal only:

```bash
sudo prlimit --pid $$ --rtprio=99 --memlock=unlimited
```

## Compile the Unitree Legged SDK and the Aliengo HAL

### Easiest: compile with the launcher

From the repository root, with your conda/pixi environment activated, just run (after the [network configuration](#network-configuration)):

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
  -DCMAKE_CXX_STANDARD_INCLUDE_DIRECTORIES=$CONDA_PREFIX/include \
  "-DCMAKE_EXE_LINKER_FLAGS=-L$CONDA_PREFIX/lib -Wl,-rpath,$CONDA_PREFIX/lib"
cmake --build build
cd ..
```

The last three flags let cmake 4 configure the SDK and let the conda compilers find the conda LCM, so the CMakeLists.txt of **unitree_legged_sdk** does not need to be modified. There is no install step.

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


## Network configuration

1. Connect Aliengo and the computer using an Ethernet cable. Then, open the network settings, find the network interface to which the robot is connected. In IPv4 setting, **change the IPv4 mode to manual, set the address to a free IP of the robot network (e.g. 192.168.123.162), and set the mask to 255.255.255.0**. Do not use 192.168.123.10 (the Aliengo control board, which the HAL talks to via UDP on port 8007) or 192.168.123.161 (the Aliengo onboard computer). After completion, click apply and wait for the network to reconnect.

2. Then, use the command **ifconfig** to view the network interface that the robot connected **(e.g. enp3s0)**:
```bash
ifconfig
```


3. Then open the file unitree_ros2_connect (`launch_aliengo_hal.py` sources it, to set up ROS 2 for the topics of the HAL)
```bash
sudo gedit unitree_ros2_connect.bash
```

4. ...and write inside your interface name found in step 2 instead of **enp3s0**
```bash
export CYCLONEDDS_URI='<CycloneDDS><Domain><General><Interfaces>
                            <NetworkInterface name="enp3s0" priority="default" multicast="default" />
                        </Interfaces></General></Domain></CycloneDDS>'
```


5. Ensure that the network of the robot is connected correctly by opening a terminal and writing:
```bash
ping 192.168.123.10
```


6. **Note that in every terminal where you launch your other scripts, you need to source unitree_ros2_connect.bash first. Put it in .bashrc as an alias!**
```bash
gedit .bashrc
alias unitree_ros2_connect='source unitree_ros2_connect.bash'
Restart the terminal!!!!
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
