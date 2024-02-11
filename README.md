Create virtual environment
```sh
python3 -m env .venv
```

Activate virtual environment
```sh
source .venv/bin/activate
```

Install pre commit hooks
```sh
python -m pip install pre-commit
```

Install Django
```sh
python -m pip install Django
```

Create Django project
```sh
mkdir src
cd src
django-admin startproject config .
```

Create Django application
```sh
python manage.py startapp lentapp
```

Start development server
```sh
python manage.py runserver
```

Migrate after model changes, example:
```sh
# Create migration
python manage.py makemigrations lentapp

# Check which SQL commands would be executed by the migration
python manage.py sqlmigrate lentapp 0001

# Check if Django finds any issues
python manage.py check

# Execute the migration
python manage.py migrate
```

Environment variables

HOST: comma-separated hosts, e. g. 'localhost,127.0.0.1'
SECRET_KEY: Django secret key, keep it secret!
DEBUG: Django is set to debug mode of environmental is set to 'ON'
DB_FILE_PATH: path to database file including file name

Docker for prod environment

Use docker compose to run the Django sever in production. Supply a .env.prod file containing the necessary environment variables. The database file needs to be located (or will be created) in the data directory from where you start the application.
