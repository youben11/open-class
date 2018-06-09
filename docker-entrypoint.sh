cd $APP_PATH

# check if the database is ready
sleep 10

# create tables
echo "Creating Database and Tables"
./manage makemigrations
./manage migrate
echo "DB and Tables created"

# create admin user
echo "Creating the admin user"
echo /create_superuser.py | ./manage.py shell
echo "Admin user created"

# run the server
echo "Starting the server..."
./manage.py runserver 0.0.0.0:8000
