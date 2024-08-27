# Using official Python image as base image
FROM python:3.8 as root

# Set environment variables
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Initialize working directory
RUN mkdir -p /mediapipe_model_maker && ls -la /mediapipe_model_maker
WORKDIR /mediapipe_model_maker

# Turn off interactivity
ENV DEBIAN_FRONTEND=noninteractive

# Install useful tools
RUN apt-get update && apt-get install -y git git-lfs ssh python3 python3-pip libgl1-mesa-glx

# Install mediapipe-model-maker and its requirements
RUN pip install --upgrade pip
RUN pip install mediapipe-model-maker --timeout=1000

# Add docker user with same UID and GID as your host system
# (copied from https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#_creating-a-nonroot-user)
FROM root as image-nonroot
ARG USERNAME=docker
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
# Switch from root to user
USER $USERNAME
