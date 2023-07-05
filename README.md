# gnss_localizer
# traffic_light_bridge
This package provides a simple implementation to send gnss localization information in CARLA to Autoware Universe. You can remap the input topic of ekf_localizer node in autoware to the topic published by this package to use the gnss localization information in CARLA directly, instead of using the ndt_scan_matcher localizer node in autoware.

## Prerequisites

Before using this package, ensure that you have the following prerequisites installed:

- ROS2 (Robot Operating System)
- CARLA simulator
- AutoWare Universe
- Follow Dr. Hatem's instructions to install the [Autoware-CARLA bridge and open planner](https://www.youtube.com/watch?v=EFH-vVxn180)
- tmux

## Installation

1. Follow the [doc](https://docs.ros.org/en/foxy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html) to create a ROS2 workspace
2. Clone this repository into your src folder under your workspace
    ```shell
    cd <your_workspace>/src
    ```
3. Build your workspace using `colcon build --symlink-install`

## Configuration
1. Change the paths in launch_script.sh to your own paths of Carla, autoware folder, current workspace
2. Modify remapping in your `autoware/src/universe/autoware.universe/launch/tier4_localization_launch/launch/pose_twist_fusion_filter/pose_twist_fusion_filter.launch.xml` file to remap the input topic of ekf_localizer node to the topic published by this package: "/localization/pose_estimator/gnss/pose_with_covariance"

## Usage
1. Launch Carla and Autoware
2. Launch the traffic_light_bridge by running launch_script.sh
    ```shell
    ./launch_script.sh
    ```