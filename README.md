# What is OpenClass?

OpenClass is a web app that promote information sharing through organised workshops.

![home](/imgs/home.png)

### Instalation
OpenClass was developed to be mainly deployed using Docker, the following instructions will guide you to deploy OpenClass on a machine that has Docker already installed. Please visit this [link]() if you don't have Docker installed yet.

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

### How it works?
At the time that you start the server, your machine should have port 80 listening to receive HTTP requests.

![deployment diagram](/imgs/deployment.png)

### Configuration
