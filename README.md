# SnowCrash

A security project for 42 school

## Installation

### Set up the SnowCrash VM

This Virtual Machine image is provided by 42.

Create a linux virtual machine with the iso with the virtualization software of your choice, such as Oracle VM VirtualBox.
Change network settings to Bridge Network.

The VM will load and display an IP address that you will need to fill in the docker-compose.yml.

### Set up the snowcrash study project

Clone the project directory

```
git clone https://github.com/mathyba/snowcrash.git
```

Full set-up is provided with Docker and Docker-Compose
If you don't have these installed, check out the official [Docker](https://docs.docker.com/get-docker/) and [Docker-Compose](https://docs.docker.com/compose/install/) doc and follow the guidelines for your distribution.

### Configuration

In the docker-compose.yml:
- change "VM" env variable for the VM's IP address obtained in the sction Set up the SnowCrash VM above.
- change "CONTAINER" env variable for the one of the network interface (wifi or physical) chosen for the bridge network, as specified in the VM settings. 
Run `ifconfig` to list the interfaces.

## Usage

### Running the main "solver" container

Following commands should be run at the root level of the project directory:

Create all services and rebuild images if necessary:

```
docker-compose up --no-start --build
```

Run snow-crash project container in interactive mode:

```
docker-compose run solver
```

From there, you will have access to all the tools and config necessary to solve the challenge, as well as scripts automatizing level resolution.

---

If you want to handle the solver container without using docker-compose, here are some useful commands.
In this case, you should uncomment the environment variables in the Dockerfile

Build the docker image:

```
docker build . -t "snowcrash-img"
```

Run the container and access project directory:

```
docker run -v $(pwd):/snowcrash/snowcrash --net host -ti snowcrash-img
```

- Volumes give access to local project directory from within the container. This makes it possible to modify files without reloading the container.
- Hosts ethernet are made visible from within the container, so that the container may communicate with the VM

## Exercice resolution

Contrary to general practice in CTF challenges, a detailed walkthrough to solve the challenge in interactive mode is provided in each level directory.
As many solutions to this project are already available online, it was felt that this would not be detrimental to the snow-crash challenge.
Please note that explanations can be tediously thorough at times, or even leading through failed attempts before reaching the solution.
The intent has been to record major steps in the (sometimes flawed) thought process of someone with no initial knowledge nor practice in security-related topics.

### Script usage

Scripts are provided to automate each level's resolution.
Obtained level tokens will be stored, so once a level has been reached once, it may in the future be accessed directly.

To run a script:
`./python3 levelXX/Ressources/levelXX.py`

To solve the challenge, you must start on level00:
`./python3 level00/Ressources/level00.py`

Aliases will be added shortly, as well as project-wide scripts to automate cleaning of tokens and temporary files.
