FROM python:3.6-alpine

ENV app_dir_name OpenClass
ENV app_path /opt/$app_dir_name
#installing django
ADD requirements.txt $app_path
RUN pip install -r requirements.txt
#adding the django project
ADD $app_dir_name $app_path
