MediaPipe Model Maker README

Fusion-Based Utilization and Synthesis of Efficient Detections

Check out our website here for background information about the project: 
https://sites.google.com/view/projectfused

Point of Contact: Ethan Rogers, ethan.c.rogers@gmail.com

This repository contains the virtual environment used to train the object
detection models for Project FUSED. 

The main FUSED environment is located here:
https://github.com/ethanrogers15/project_fused

The ROS2 environment repository is located here:
https://github.com/ethanrogers15/project_fused_ros

To run this virtual environment, you will need Docker Desktop and VSCode with
the Remote Development & Dev Containers extensions. The virtual environments
for Project FUSED were built on a Windows laptop, but we used WSL with Ubuntu
to interface with the ROS environment. So, we recommend making sure that WSL
is set up with Ubuntu if you are using a Windows laptop. 

After cloning the repository to a directory in your file system, opening the 
directory in VSCode will result in a prompt to "build" the environment as a 
Dev Container. After starting the build, it will take 10-20 minutes to complete
the process - some of the packages take a long time to install!

Once the environment is built, make sure that the environment's Python
interpreter is in use when selecting a Python file, and you should be good to
go!

The main file is 'model_maker.py' in the 'src' directory. It takes the training
dataset and trains the object detection models that were used for the fusion
algorithm.
