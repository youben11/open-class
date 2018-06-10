# What is OpenClass?

OpenClass is a web app that promote information sharing through organised workshops.

![home](/imgs/home.png)

## Instalation
OpenClass was developed to be mainly deployed using Docker, the following instructions will guide you to deploy OpenClass on a machine that has Docker already installed. Please visit this [link](https://docs.docker.com/install/) if you don't have Docker installed yet.

#### Get the source code
First run the following command to get the Project code:
```bash
$ git clone https://github.com/youben11/open-class
```

Then change your current directory to open-class:
```bash
$ cd open-class
```

###### NOTE :
If you don't have Git installed then download the code as a zip file and unzip it in open-class directory.

#### Start the server
For a simple usage run :
```bash
$ docker-compose up
```
It should take some time the first time your run this command (it depends on your connection), docker images will be pulled and built.

## How it works?
At the time that you start the server, your machine should have port 80 listening to receive HTTP requests.

![deployment diagram](/imgs/deployment.png)

The Docker Daemon should start 3 containers when you run `docker-compose` : web, db and db_redis.
- web is the container that is running the actual Django application, it is built using the Dockerfile provided. The server is binding his HTTP port to the HTTP port of this container.

- db is running a postgres image, the PostgreSQL database is used by the web app to store many information. The server is not binding any port to this container.

- db_redis is running a redis image, the redis database store information in a key/value fashion, which make it useful for storing the web app configuration. The server is not binding any port to this container.

All this containers are connected together in a local virtual LAN and can't be accessed from the outside unless a port is binded.

## Configuration
The first time that the server is started, the admin account is created with a username='admin' and a password='openclassadmin', you should change the password via the admin panel (example: http://localhost/admin/).

##### IMPORTANT !
Don't forget to change the admin's password.
