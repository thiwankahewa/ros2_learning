import launch
from launch import LaunchDescription
from launch_ros.actions import Node
import launch_ros
import os

pkgName = 'urdfRobot'
urdfRelativePath = 'urdf/model.urdf'
rvizRelativePath = 'config/config.rviz'

def generate_launch_description():
    pkgPath = launch_ros.substitutions.FindPackageShare(package=pkgName).find(pkgName)
    urdfModelPath = os.path.join(pkgPath,urdfRelativePath)
    rvizConfigPath = os.path.join(pkgPath,rvizRelativePath)
    
    with open(urdfModelPath,'r') as infp:
        robot_desc = infp.read()
        
    params = {'robot_description':robot_desc}

    robot_state_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output = 'screen',
        parameters=[params]
        arguments=[urdfModelPath]
    )
    
    joint_state_pub = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        arguments=[urdfModelPath],
        condition=launch.conditions.IfCondition(launch.substitutions.LaunchConfiguration('gui')) 
    )
    
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rvizConfigPath],
    )
    
    return LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            'gui',
            default_value='true',
            description='Flag to enable GUI'
        ),
        robot_state_pub,
        joint_state_pub,
        rviz_node
    ])