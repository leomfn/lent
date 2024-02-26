# Lent - lend whatever to whomever

Lent is a Django application enabling its users to easily borrow an item for a specific timeslot.

![Lent Demo](https://github.com/leomfn/lent/assets/99895548/30fb6d83-8ed7-4c51-b66e-c4548fa90381)

## Development notes

### Database initialization

If you don't provide a database (e. g. from earlier usage of the program), a sqlite database file will be created at the first start of the program. This is defined in the *init.sh* shell script.

### Development environment

You'll need docker and docker compose to run the development container. You must supply a *.env.dev* file that holds the necessary environment variables (see [Environment variables](#environment-variables)).

Start the development container using `docker compose watch`. The *docker-compose.yml* file holds the configuration for the production environment, however, it is overwritten by *docker-compose.override.yml*, which holds development specific settings. [`watch`](https://docs.docker.com/compose/file-watch/) will listen to code changes made in */src* and sync the changes to the container, which the Django development server will pick up, resulting in a hot-reload.

The *Dockerfile* is set to execute *init.sh* which, if `DEBUG='ON'`, will start the development server. The server is automatically restarted when you change the local source code.

Open <http://localhost:8011> in your local browser to view and test the application's frontend.

### Production environment

Use docker compose to run the Django sever in production. Supply a *.env.prod* file containing the necessary environment variables (see [Environment variables](#environment-variables)). The database file needs to be located (or will be created) in the *data* directory from where you start the application. The directory must also contain a *static* folder. The *init.sh* script is run when the container has started. This will execute `python manage.py collectstatic`, transferring files to the static folder.

### Environment variables

```sh
HOST                # comma-separated hosts, e. g. 'localhost,127.0.0.1'
SECRET_KEY          # Django secret key, keep it secret!
DEBUG               # Django is set to debug mode if environmental is set to 'ON', while setting it to 'OFF' will activate production mode
DB_FILE_PATH        # path to database file
STATIC_FILES_PATH   # path to static files like pictures
TIME_ZONE           # Time zone to be used for the frontend, should reflect the time zone of userbase/items (e. g. 'Europe/Berlin')
LANGUAGE_CODE       # sets locale for displaying date, time formats etc. (e. g. 'en-us' or 'de-de'), ⚠️ doesn't work yet for input format in form fields, depends on browser locale
DJANGO_ADMIN_USERNAME   # django superuser username which is set the first time you initialize the app
DJANGO_ADMIN_EMAIL      # django superuser email addresss which is set the first time you initialize the app
DJANGO_ADMIN_PASSWORD   # django superuser password which is set the first time you initialize the app
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
