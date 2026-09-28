import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    sick_scan_pkg = get_package_share_directory('sick_scan_xd')
    launch_file_path = os.path.join(sick_scan_pkg, 'launch', 'sick_tim_5xx.launch')

    # Node for the LEFT LiDAR (.96)
    lidar_left = Node(
        package='sick_scan_xd',
        executable='sick_generic_caller',
        name='left_2D',
        arguments=[
            launch_file_path,
            'hostname:=192.168.0.96',
            'frame_id:=left_2D',
            'nodename:=left_2D'
        ],
        remappings=[
            ('scan', 'left')  # This changes the output topic from /scan to /left
        ],
        output='screen'
    )

    # Node for the RIGHT LiDAR (.97)
    lidar_right = Node(
        package='sick_scan_xd',
        executable='sick_generic_caller',
        name='right_2D',
        arguments=[
            launch_file_path,
            'hostname:=192.168.0.97',
            'frame_id:=right_2D',
            'nodename:=right_2D'
        ],
        remappings=[
            ('scan', 'right') # This changes the output topic from /scan to /right
        ],
        output='screen'
    )

    return LaunchDescription([
        lidar_left,
        lidar_right
    ])