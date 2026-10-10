"""Start one SICK driver per SICK config installed for this build's vehicle.

Sensors_ws builds for one vehicle (src/build.sh <vehicle>). Each SICK sensor in that
vehicle's sensors.yaml picks a config file (a sick_scan_xd .launch file, e.g.
launch/virya_tim581_left_AMR50_Canopy.launch); sensor_configs installs it as
share/sensor_configs/vehicle/sick_scan_xd/<sensor name>.launch. This starts one
sick_generic_caller per installed file, named after the sensor: one scanner or n,
TiM581 or LD-MRS, all launched the same way. The file name is kept so whatever
started the two-scanner launch still starts this one.
"""
from pathlib import Path

from ament_index_python.packages import get_package_share_directory, PackageNotFoundError
from launch import LaunchDescription
from launch_ros.actions import Node


def vehicle_sick_configs():
    try:
        share = Path(get_package_share_directory('sensor_configs'))
    except PackageNotFoundError:
        raise RuntimeError('sensor_configs is not installed: build Sensors_ws with '
                           'src/build.sh <vehicle>')
    configs = sorted((share / 'vehicle' / 'sick_scan_xd').glob('*.launch'))
    if not configs:
        raise RuntimeError(
            f'no SICK config installed for vehicle {(share / "vehicle_name").read_text().strip()} '
            f'({share / "vehicle" / "sick_scan_xd"}): check its sensors.yaml')
    return configs


def generate_launch_description():
    return LaunchDescription([
        Node(package='sick_scan_xd', executable='sick_generic_caller', name=config.stem,
             output='screen', arguments=[str(config)])
        for config in vehicle_sick_configs()
    ])
