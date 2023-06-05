from setuptools import setup

package_name = 'measure_process_ros2_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kiko',
    maintainer_email='fma527@ual.es',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'measure_process = measure_process_ros2_pkg.measure_process:main',
            'record_cpu_usage = record_cpu_usage_pkg.record_cpu_usage:main'
        ],
    },
)
