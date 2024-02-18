# Lent - lend whatever to whomever

Lent is a Django application enabling its users to easily borrow an item for a specific timeslot.

![output](https://github.com/leomfn/lent/assets/99895548/67630111-010d-40b0-a3a3-1b3fd787493c)

## Development notes

### Setup

Create and activate virtual environment
```sh
python3 -m env .venv && source .venv/bin/activate
```

Install dependencies
```sh
pip install -r requirements-dev.txt
```

Install pre commit hooks
```sh
python -m pip install pre-commit
```

Start development server
```sh
python src/manage.py runserver
```

### Database migration

Migrate after model changes, example:
```sh
# Create migration
python src/manage.py makemigrations lentapp

# Check which SQL commands would be executed by the migration
python src/manage.py sqlmigrate lentapp 0001

# Check if Django finds any issues
python src/manage.py check

# Execute the migration
python src/manage.py migrate
```

### Environment variables

* `HOST`: comma-separated hosts, e. g. 'localhost,127.0.0.1'
* `SECRET_KEY`: Django secret key, keep it secret!
* `DEBUG`: Django is set to debug mode of environmental is set to 'ON'
* `DB_FILE_PATH`: path to database file including file name
* `STATIC_FILES_PATH`: path to static files like pictures

### Docker for production environment

Use docker compose to run the Django sever in production. Supply a .env.prod file containing the necessary environment variables. The database file needs to be located (or will be created) in the data directory from where you start the application.
