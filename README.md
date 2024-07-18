# Installing Docker and Docker Compose on Ubuntu

This guide will help you install Docker and Docker Compose on an Ubuntu system.

## Prerequisites

- A system running Ubuntu (preferably 20.04 LTS or later)
- A user account with `sudo` privileges

## Installing Docker

1. **Update the package index:**

    ```bash
    sudo apt update
    ```

2. **Install required packages:**

    ```bash
    sudo apt install apt-transport-https ca-certificates curl software-properties-common
    ```

3. **Add Docker's official GPG key:**

    ```bash
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    ```

4. **Set up the Docker repository:**

    ```bash
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    ```

5. **Update the package index again:**

    ```bash
    sudo apt update
    ```

6. **Install Docker CE:**

    ```bash
    sudo apt install docker-ce
    ```

7. **Check the Docker service status:**

    ```bash
    sudo systemctl status docker
    ```

8. **Add your user to the `docker` group to run Docker commands without `sudo`:**

    ```bash
    sudo usermod -aG docker $USER
    ```

9. **Log out and log back in to apply the group changes.**

## Installing Docker Compose

1. **Download Docker Compose:**

    ```bash
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    ```

2. **Apply executable permissions to the Docker Compose binary:**

    ```bash
    sudo chmod +x /usr/local/bin/docker-compose
    ```

3. **Verify the installation:**

    ```bash
    docker-compose --version
    ```

## Verifying Docker and Docker Compose Installation

1. **Run a simple Docker container:**

    ```bash
    docker run hello-world
    ```

    This command downloads a test image and runs it in a container. When the container runs, it prints a confirmation message.

2. **Check Docker Compose version:**

    ```bash
    docker-compose --version
    ```

    This command outputs the version of Docker Compose installed.

Congratulations! You have successfully installed Docker and Docker Compose on your Ubuntu system.

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)


