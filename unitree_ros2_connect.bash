#!/bin/bash
echo "Setup unitree ros2 environment: Remember to change inside this file the NetworkInterface"
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
#CURRENT_DIR="$(pwd)"
echo "Current dir: $CURRENT_DIR"
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export ROS_LOCALHOST_ONLY=0
# Jazzy+ (incl. lyrical) ignore ROS_LOCALHOST_ONLY: undo a LOCALHOST discovery range
# inherited from a pixi env or ros2_localhost_connect.sh, otherwise the robot is not seen.
export ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET
unset ROS_STATIC_PEERS
export ROS_DOMAIN_ID=0 # Set a unique domain ID for your local environment
export CYCLONEDDS_URI='<CycloneDDS><Domain><General><Interfaces>
                            <NetworkInterface name="enp98s0" priority="default" multicast="default" />
                        </Interfaces></General></Domain></CycloneDDS>'

# Restart the ros2 CLI daemon so it picks up the settings above. A daemon left
# over from another profile (or this one, after the interface went down) can
# stop answering, and `ros2 daemon stop` then waits on it forever.
if command -v ros2 >/dev/null 2>&1; then
    timeout -k 2 5 ros2 daemon stop || {
        echo "ros2 daemon not responding, killing it"
        pkill -KILL -f "ros2cli\.daemon\.daemonize .*--ros-domain-id ${ROS_DOMAIN_ID:-0} "
        sleep 1
    }
    ros2 daemon start
else
    echo "ros2 not found: activate a ROS 2 env first, then restart the daemon (ros2 daemon stop; ros2 daemon start)"
fi
