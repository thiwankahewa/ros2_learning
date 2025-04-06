import os
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    robotName = "differential drive robot"

    pkgName = "gazeboRobot"
    modelRelativePath = 'model/model.xacro'
    pathModelFile = os.path.join(get_package_share_directory(pkgName), modelRelativePath)


    robotDescription = xacro.process_file(pathModelFile).toxml()

    gazebo_rosPkgLaunch = PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py'))

    
    gazeboLaunch = IncludeLaunchDescription(
        gazebo_rosPkgLaunch,
        launch_arguments={
            'gz_args':['-r -v -v4 empty.sdf'],
            'on_exit_shutdown': 'true'}.items())
    
    #gazebo node
    spawnModeNodeGazebo = Node(   
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', robotName,
            '-topic','robot_description'],
        output='screen')
    
    #robot state publisher node
    robotStatePublisherNode = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robotDescription,
            'use_sim_time': True}])
    
    #ros2 gazebo bridge node
    bridge_params = os.path.join(
        get_package_share_directory(pkgName),
        'parameters',
        'bridge_parameters.yaml')
    
    gazeboRosNode = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_params}',],
        output='screen',)
    
    launchDescriptionObject = LaunchDescription()

    launchDescriptionObject.add_action(gazeboLaunch)

    launchDescriptionObject.add_action(spawnModeNodeGazebo)
    launchDescriptionObject.add_action(robotStatePublisherNode)
    launchDescriptionObject.add_action(gazeboRosNode)

    return launchDescriptionObject
    
    
    

        
    
