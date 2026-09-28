import os
import sys
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument

def generate_launch_description():

    ld = LaunchDescription()
    sick_scan_pkg_prefix = get_package_share_directory('sick_scan_xd')

    # Points to the twin XML — note: hardcoded name, NOT derived from __file__
    # because this .py is the twin wrapper, not a 1:1 named pair
    launch_file_path = os.path.join(sick_scan_pkg_prefix, 'launch/sick_tim_5xx_twin.launch')

    # Collect any extra commandline args in name:=value syntax
    extra_args = [arg for arg in sys.argv if len(arg.split(":=")) == 2]

    ROS_DISTRO = os.environ.get('ROS_DISTRO')

    # RIGHT LiDAR - 192.168.0.96
    right_arguments = [launch_file_path, 'nodename:=sick_tim581_right'] + extra_args
    # LEFT LiDAR  - 192.168.0.97
    left_arguments  = [launch_file_path, 'nodename:=sick_tim581_left']  + extra_args

    if ROS_DISTRO[0] <= "e":
        right_node = Node(package='sick_scan_xd', node_executable='sick_generic_caller',
                          output='screen', arguments=right_arguments)
        left_node  = Node(package='sick_scan_xd', node_executable='sick_generic_caller',
                          output='screen', arguments=left_arguments)
    else:
        right_node = Node(package='sick_scan_xd', executable='sick_generic_caller',
                          output='screen', arguments=right_arguments)
        left_node  = Node(package='sick_scan_xd', executable='sick_generic_caller',
                          output='screen', arguments=left_arguments)

    ld.add_action(right_node)
    ld.add_action(left_node)
    return ld
