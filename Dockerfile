FROM python:3.6-alpine

ENV app_dir_name OpenClass
ENV app_path /opt/$app_dir_name
#installing django
ADD requirements.txt /
RUN pip install -r requirements.txt
RUN rm requirements.txt
#adding the django project
ADD $app_dir_name $app_path
