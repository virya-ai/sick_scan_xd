import os
import sys
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument

def generate_launch_description():

    ld = LaunchDescription()
    sick_scan_pkg_prefix = get_package_share_directory('sick_scan_xd')

    right_launch = os.path.join(sick_scan_pkg_prefix, 'launch/virya_tim581_right.launch')
    left_launch  = os.path.join(sick_scan_pkg_prefix, 'launch/virya_tim581_left.launch')

    ROS_DISTRO = os.environ.get('ROS_DISTRO')

    if ROS_DISTRO[0] <= "e":
        right_node = Node(package='sick_scan_xd', node_executable='sick_generic_caller',
                          output='screen', name='sick_tim581_right', arguments=[right_launch])
        left_node  = Node(package='sick_scan_xd', node_executable='sick_generic_caller',
                          output='screen', name='sick_tim581_left', arguments=[left_launch])
    else:
        right_node = Node(package='sick_scan_xd', executable='sick_generic_caller', name='sick_tim581_right',
                          output='screen', arguments=[right_launch])
        left_node  = Node(package='sick_scan_xd', executable='sick_generic_caller', name='sick_tim581_left',
                          output='screen', arguments=[left_launch])

    ld.add_action(right_node)
    ld.add_action(left_node)
    return ld
