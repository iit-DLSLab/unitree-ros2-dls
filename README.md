## Overwiew
This repo connects to many unitree robots using ros2. It uses: 

- [unitree_ros2](https://github.com/unitreerobotics/unitree_ros2) for controlling **GO2**, **A2**, **B2**
- [unitree_legged_sdk](https://github.com/unitreerobotics/unitree_legged_sdk) for **Aliengo**
- [z1_sdk](https://github.com/iit-DLSLab/z1_sdk)/[z1_controller](https://github.com/unitreerobotics/z1_controller) for the **Z1** arm. 

We add on top of these some [messages](./ros2_ws/src/dls2_interface/msg/) to be compatible with different **dls repositories**, like: 

- [basic-locomotion-isaaclab](https://github.com/iit-DLSLab/basic-locomotion-isaaclab) for RL locomotion
- [get-up-isaaclab](https://github.com/iit-DLSLab/get-up-isaaclab) for RL get-up task
- [sim2real-robot-identification](https://github.com/iit-DLSLab/sim2real-robot-identification) for IsaacLab and Mujoco identification
- [Quadruped-PyMPC](https://github.com/iit-DLSLab/Quadruped-PyMPC) for MPC
- [muse](https://github.com/iit-DLSLab/muse/tree/unitree_sdk) for State Estimation

and many others.. Check our github!


## Dependencies

**Note that if you are using one of our other repos with conda, you will likely have everything you need installed. In that case, just activate that conda env!**

1. install [pixi](https://pixi.prefix.dev/latest/installation/).

2. activate the environment from the root of this repo by doing:

```bash
pixi shell -e humble # humble
pixi shell -e lyrical # lyrical
```

3. Initialise the submodules:

```bash
git submodule update --init --recursive
```

## Setup Go2, B2, A2

Follow [README_unitree_ros2](./README_unitree_ros2.md) to install the things needed for GO2, B2 and A2.

## Setup Aliengo

Follow [README_unitree_legged_sdk](./README_unitree_legged_sdk.md) to install the things needed for Aliengo.

## Setup Z1 arm

Follow [README_unitree_z1](./README_unitree_z1.md) to install the things needed for Z1 arm.

## How to contribute

PRs are very welcome (search for **TODO** in the issue, or add what you like)!

## Maintainer

This repository is maintained by [Giulio Turrisi](https://github.com/giulioturrisi).
