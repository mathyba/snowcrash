FROM ubuntu:latest

# Uncomment to build image for direct use (without docker-compose)

#ENV HOST "localhost"
#ENV PORT 4242
#ENV PYTHONPATH "$PYTHONPATH:/snowcrash"
#ENV PATH "$PATH:/usr/lib/python3.8/site-packages"
#ENV REMOTE_PATH "/snowcrash"
#ENV LOG_LEVEL "info"

# Required to prevent interactive prompt while installing dependencies
ENV ARCH=$(arch)
ENV TERM=linux 
ENV HOME=/home/snowcrash
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && apt-get install -y \
        dialog \
        gdbserver


# Install dependencies
RUN apt-get update -y && apt-get install -y --fix-missing \
        sshpass \
        git \
        libcapstone3 \
        python3.8 \
        python3-pip \
        python3-dev \
        libssl-dev \
        libffi-dev \
        build-essential \
        net-tools \
        tshark \
        john \
        gdb \
        netcat \
    && python3 -m pip install --upgrade pip \
    && python3 -m pip install git+https://github.com/Gallopsled/pwntools.git@stable \
    && python3 -m pip install pylint black

RUN useradd -ms /bin/bash snowcrash
RUN echo 'PS1="[\u@docker]\033[0;33m \w # \033[0;0m"' > /etc/bash.bashrc
USER snowcrash
WORKDIR /home/snowcrash

