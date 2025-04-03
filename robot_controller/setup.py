from setuptools import find_packages, setup

package_name = 'robot_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/launch.py']),
        
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='thiwanka',
    maintainer_email='thiwanka@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "test_node = robot_controller.firstNode:main",
            "drawCircle = robot_controller.drawCircle:main",
            "getPose = robot_controller.getPose:main",
            "turtleController = robot_controller.turtleController:main",
            
        ],
    },
)
