#!/bin/sh

cd $APP_PATH

# check if the database is ready
sleep 10

# create tables
echo "Updating Database Tables"
./manage.py makemigrations
./manage.py migrate
echo "The Database has been updated"

# create admin user
echo "Creating the admin user"
cat /create_superuser.py | ./manage.py shell
echo "Admin user created"

# run the server
echo "Starting the server..."
./manage.py runserver 0.0.0.0:8000
