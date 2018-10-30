FROM python:3.6-alpine

ENV APP_DIR_NAME OpenClass
ENV APP_PATH /opt/$APP_DIR_NAME

#installing postgres requirements
RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev postgresql-dev postgresql
#Pillow requirements
RUN apk update \
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

#installing django
COPY requirements.txt /
RUN pip install -r requirements.txt
RUN rm requirements.txt

#adding entrypoint scripts
COPY docker-entrypoint.sh /
COPY create_superuser.py /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

#adding the django project
RUN mkdir -p $APP_PATH
COPY $APP_DIR_NAME $APP_PATH
