FROM python:3.6-alpine

ENV app_dir_name OpenClass
ENV app_path /opt/$app_dir_name
#installing django
ADD requirements.txt /
RUN pip install -r requirements.txt
RUN rm requirements.txt
#adding the django project
EXPOSE 8000
ADD $app_dir_name $app_path

WORKDIR $app_path
CMD python manage.py runserver 0.0.0.0:8000

