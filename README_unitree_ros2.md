## Install Unitree ROS2 package

First, initialise the submodules:

```bash
git submodule update --init --recursive
```

### Easiest: compile with the launchers

From the repository root, with your conda/pixi environment activated, just run (after the [network configuration](#network-configuration)):

```bash
python3 launch_go2_hal.py # GO2
python3 launch_a2_hal.py  # A2
```

The first time, the launchers compile everything GO2 and A2 need (the unitree messages in **unitree_ros2/cyclonedds_ws**, and the ROS 2 packages `dls2_interface`, `go2_hal` and `a2_hal`) and then start the HAL. The next times they only start the HAL. The GO2 and A2 HALs are always compiled together. If a build folder already exists, the launchers first ask whether to delete it and rebuild from scratch.

### What the launchers do, by hand

From the repository root, with your conda/pixi environment activated:

1. Compile the unitree messages in **unitree_ros2/cyclonedds_ws** (the launchers do it only if `unitree_ros2/cyclonedds_ws/install` does not exist):

```bash
cd unitree_ros2/cyclonedds_ws
colcon build # Compile all packages in the workspace
cd ../..
```

If you have any problem complaining **rosidl_generate_interfaces** (likely), search globally from **cmake_minimum_required(VERSION** and bump each version to 3.15

2. Compile the DLS2 messages and the GO2 and A2 HALs in **ros2_ws** (the launchers do it only if `ros2_ws/install/dls2_interface`, `ros2_ws/install/go2_hal` or `ros2_ws/install/a2_hal` do not exist):

```bash
source unitree_ros2/cyclonedds_ws/install/setup.bash
cd ros2_ws
colcon build --packages-select dls2_interface go2_hal a2_hal
cd ..
```

3. Start the HAL:

```bash
source unitree_ros2/cyclonedds_ws/install/setup.bash
source unitree_ros2_connect.bash
source ros2_ws/install/setup.bash
./ros2_ws/install/go2_hal/bin/go2_hal # GO2
./ros2_ws/install/a2_hal/bin/a2_hal   # A2
```

To rebuild from scratch, delete the build folders first (this is what answering `y` to the launchers does):

```bash
rm -rf unitree_ros2/cyclonedds_ws/build unitree_ros2/cyclonedds_ws/install unitree_ros2/cyclonedds_ws/log
rm -rf ros2_ws/build ros2_ws/install ros2_ws/log
```


## Network configuration

1. Connect Unitree robot and the computer using an Ethernet cable. Then, open the network settings, find the network interface to which the robot is connected. In IPv4 setting, **change the IPv4 mode to manual, set the address to 192.168.123.99 for GO2, 192.168.123.222 for A2, and set the mask to 255.255.255.0**. After completion, click apply and wait for the network to reconnect.

2. Then, use the command **ifconfig** to view the network interface that the robot connected **(e.g. enp3s0)**:
```bash
ifconfig
```


3. Then open the file unitree_ros2_connect
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
source unitree_ros2_connect.bash
ros2 topic list
```


6. **Note that in every terminal where you launch your other scripts, you need to source this file first. Put it in .bashrc as an alias!** 
```bash
gedit .bashrc
alias unitree_ros2_connect='source unitree_ros2_connect.bash'
Restart the terminal!!!!
```


## Running the quadruped hal
Open a terminal and input:
```bash
unitree_ros2_connect
```
**Note that in every terminal where you launch your other scripts, you need to source this file first. Put it in .bashrc as an alias!**

Then run in the terminal:
```bash
python3 launch_go2_hal.py # GO2
python3 launch_a2_hal.py  # A2
```
