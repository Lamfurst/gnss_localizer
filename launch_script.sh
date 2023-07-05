#!/bin/bash

tmux split-window -h
tmux send-keys "source /home/artemis/Workspace/autowarefoundation/carla-autoware-universe/autoware/install/setup.bash" C-m
tmux send-keys "source /home/artemis/personal_autoware_ws/install/setup.bash" C-m
tmux send-keys "ros2 run gnss_localizer gnss_localizer" C-m


