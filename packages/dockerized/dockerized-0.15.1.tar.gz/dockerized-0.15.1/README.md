dockerized 🏗❤️
================

Easily Docker-ize your build/development environment and seamlessly run commands inside it.

_dockerized_ is a tool for seamlessly executing commands in a container. It takes care of the details so you can run a command in a container as if it was running on your machine - just prepend any command with `dockerized exec` to have it run in the container.

See https://benzaita.github.io/dockerized-cli/index.html
# Getting Started

Install _dockerized_:
```shell
$ pip install dockerized
```

Initialize your environment:
```shell
$ dockerized init
$ echo FROM python:3.9 > .dockerized/Dockerfile.dockerized
```

or use an example:
```shell
$ dockerized init --from https://github.com/benzaita/dockerized-example-python.git
```

Then run a command inside that environment:
```shell
$ dockerized exec python --version
...
Python 3.9.0
```

Or drop into an interactive shell inside the environment:
```shell
$ dockerized shell
# python --version
Python 3.9.0
```

# Examples

See the [examples wiki page](https://github.com/benzaita/dockerized-cli/wiki/Examples).

# Advanced Topics

 - [Caching the dockerized image](https://github.com/benzaita/dockerized-cli/wiki/Caching-the-'dockerized'-image)
 - [Using environment variables](https://github.com/benzaita/dockerized-cli/wiki/Environment-Variables)

# FAQ

## Why not `docker run` or `docker exec`?

Fair question! After all _dockerized_ is just a wrapper for Docker. You can definitely use `docker run` or `docker exec` but there are a few details you'd have to take care of:

**Rebuilding the Docker image:** after changing the `Dockerfile`, you need to run `docker build` before running `docker run` again. When iterating on the `Dockerfile` this can become a pain.

With _dockerized_ you just do `dockerized exec`.

**Volumes and working directory**: to allow the developer to run commands from arbitrary locations within the project, you probably want to mount the project root into the container. Manually running `docker run -v $PWD:...` one time and `docker run -v $PWD/..:...` another time, or adding some script to do this for you.

With _dockerized_ you just do `dockerized exec`.

**Running Docker Compose:** almost every project has integration tests. Running them locally usually means running Docker Compose. Now you need to run `docker-compose up` before running `docker run`. Besides being annoying, see also "Port contamination" below.

With _dockerized_ you just do `dockerized exec`.

**"Port contamination":** many people run their tests on the host, against dependencies (think PostgreSQL for example) running in containers. Since the tests need to access the PostgreSQL port, they expose this port to the host. When you are working on multiple projects these exposed ports start conflicting and you have to `docker-compose stop` one project before `docker-compose start` the other.

With _dockerized_ you just do `dockerized exec`.
