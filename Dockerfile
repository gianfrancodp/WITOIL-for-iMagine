# Dockerfile may have following Arguments:
# tag - tag for the Base image, (e.g. 2.9.1 for tensorflow)
# branch - user repository branch to clone, i.e. test (default: main)
#
# To build the image:
# $ docker build -t <dockerhub_user>/<dockerhub_repo> --build-arg arg=value .
# or using default args:
# $ docker build -t <dockerhub_user>/<dockerhub_repo> .
#
# Be Aware! For the Jenkins CI/CD pipeline, 
# input args are defined inside the JenkinsConstants.groovy, not here!

ARG tag=base

# Base image, e.g. tensorflow/tensorflow:2.x.x-gpu
FROM ai4oshub/witoil-for-imagine:${tag}

LABEL maintainer='Elnaz Azmi, Fahimeh Alibabaei, Igor Atake, Gabriele Accarino, Marco Decarlo, Giovanni Coppini'
LABEL version='0.0.1'
# Medslik-II Oil fate lagrangian model

# What user branch to clone [!]
ARG branch=main

# Install Ubuntu packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Update python packages
# [!] Remember: DEEP API V2 only works with python>=3.6
RUN python3 --version && \
    pip3 install --no-cache-dir --upgrade pip setuptools wheel

# Set LANG environment
ENV LANG=C.UTF-8

# Set the working directory
WORKDIR /srv

# Disable FLAAT authentication by default
ENV DISABLE_AUTHENTICATION_AND_ASSUME_AUTHENTICATED_USER=yes

# Initialization scripts
# deep-start can install JupyterLab or VSCode if requested
RUN git clone https://github.com/ai4os/deep-start /srv/.deep-start && \
    ln -s /srv/.deep-start/deep-start.sh /usr/local/bin/deep-start

# Necessary for the Jupyter Lab terminal
ENV SHELL=/bin/bash

# Install rclone (needed if syncing with NextCloud for training; otherwise remove)
RUN curl -O https://downloads.rclone.org/rclone-current-linux-amd64.deb && \
    dpkg -i rclone-current-linux-amd64.deb && \
    apt install -f && \
    mkdir /srv/.rclone/ && \
    touch /srv/.rclone/rclone.conf && \
    rm rclone-current-linux-amd64.deb && \
    rm -rf /var/lib/apt/lists/*
ENV RCLONE_CONFIG=/srv/.rclone/rclone.conf

# Install user app
RUN git clone -b $branch --depth 1 https://github.com/ai4os-hub/witoil-for-imagine && \
    cd witoil-for-imagine && \
    git submodule update --init --recursive --remote && \
    pip3 install --no-cache-dir -e .

# (force) remove WITOIL_iMagine/data/{gebco|gshhs} directories
# and link to the Gebco Bathymetry and GSHHS Coastline directories
# already placed in the "base" image (/data/{gebco|gshhs})
RUN cd /srv/witoil-for-imagine/WITOIL_iMagine/data/ && \
    rm -rf gebco && rm -rf gshhs && \
    ln -s /data/gebco gebco && \
    ln -s /data/gshhs gshhs

# Open ports: DEEPaaS (5000), Monitoring (6006), Jupyter (8888)
EXPOSE 5000 6006 8888

# Add the entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/srv/witoil-for-imagine" \
    --uid "${UID}" \
    appuser

RUN chown -R appuser:appuser /srv

###
# In princple, shouldn't be a problem to run under non-root user
# except development where additional linux packages might need to be installed.
# Nevertheless, comment the line below for now and run under root
###
#USER appuser
###

# Launch deepaas in /srv/witoil-for-imagine
# WORKDIR /srv might be needed for jupyter or vscode
# CMD ["sh","-c","cd /srv/witoil-for-imagine && deep-start"]

# Set the entrypoint
ENTRYPOINT ["entrypoint.sh"]