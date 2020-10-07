# Install Hector SLAM

- In terminal:

```
sudo apt install ros-melodic-hector-slam
roscd hector_mapping
cd launch
gedit mapping_default.launch
```

- In mapping_default.launch:

- change 
<arg name="odom_frame" default="nav"/>
to
<arg name="odom_frame" default="base_footprint"/>

- add
<param name="tf_map_scanmatch_transform_frame_name" value="$(arg tf_map_scanmatch_transform_frame_name)" />
