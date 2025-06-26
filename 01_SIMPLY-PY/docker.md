# DOCKER & CONTAINERIZATION

## BEFORE DOCKER

Before Docker, applications had to be deployed and shipped individually, with resources allocated separately for each application on the server. This inefficient approach of using separate operating systems and resources for individual applications hindered application scalability. VMware addressed this resource management challenge by using a Hypervisor to distribute server resources across multiple virtual machines within the same operating system and server.  

A hypervisor (Virtual Machine Monitor) is a software layer that enables virtual machines to run on host hardware. Type 1 hypervisors (like VMware ESXi) run directly on hardware, while Type 2 (like VirtualBox) run on top of an operating system. They manage resource allocation between VMs, ensuring efficient hardware utilization and isolation.

However, this virtualization approach still required significant overhead since each virtual machine needed its own operating system. This led to the development of containerization technologies like Docker, which provide a more lightweight solution by sharing the host operating system's kernel while maintaining isolation between applications. Docker containers package applications with their dependencies, making them portable and efficient to deploy across different environments.

## HOW DOES VIRTUAL MACHINES AND DOCKER CONTAINER WORKS ?

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/a2e99cd1-082a-41bf-812d-83187d62cefe/image.png)

An application on a VM requires a guest OS and thus an underlying hypervisor to run. The virtual machines created by Hypervisor have their own operating system and do not use the host’s operating system. They  have some resources allocated. Containerization is an efficient method for deploying the applications where the container encapsulates an application with its own base operating environment.  It can be placed on any host machine without special configuration, removing the issue of dependencies and package conflicts. 

VM is a hardware virtualization whereas containerization is OS virtualization. Essentially, containerization is a lightweight and go-to approach to virtualization. 

## What is  Docker?

Docker is a container platform that allows you to build, test, and deploy applications quickly. A developer defines all the applications and their dependencies in a Dockerfile, which is then used to build Docker images that define Docker containers. This process ensures that your application will run in any environment.

**Docker Architecture:**

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/9a71a173-3481-40c6-9bb6-ada2448b6ffd/image.png)

Docker usage the client-server architecture. The docker client talks to the docker daemon on server which does the job of building, running and distributing your Docker containers. 

## Docker Concepts & Terminologies

### Docker Daemon

### Docker Client

### Docker Registries

### Docker-file

### Docker Image

### Docker Installation in Linux

One of these **Ubuntu** version will be required for the installation of docker engine in Ubuntu and its derivatives like Pop OS and Linux Mint. 

- Ubuntu Oracular 24.10
- Ubuntu Noble 24.04 (LTS)
- Ubuntu Jammy 22.04 (LTS)
- Ubuntu Focal 20.04 (LTS)

**Commands**

1. Uninstalling conflicting packages:

    
    `for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done`
    
2. Set up the docker **apt** repository in the host machine for installation through repository: 

    
    `sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc`
    
    `echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update`
    
    If you use an Ubuntu derivative distribution, such as Linux Mint, you may need to use `UBUNTU_CODENAME` instead of `VERSION_CODENAME`.
    
3. Install the docker packages using the following command: 
    
    `sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`