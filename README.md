# power-rankings-django

This is an example project demonstrating how to set up a simple
power rankings application using the Django framework.
**These instructions are for a mac with docker desktop already installed**.
For a database, we will use postgresql (with docker). To install dependencies,
first confirm that you are using a Python 3.6 installation with `python -V`
(I suggest using pyenv if you find that your python version is not 3.6).
Then, `python -m venv env && source env/bin/activate`, then (from the new shell) 
`python -m pip install requirements.txt`

## Configuring your environment

Although it's not "necessary" for this case, it's good practice to not expose your credentials.
For that reason, most of the "credentials" for this project aren't committed as source code. 
Instead, there's a redacted copy at `power_rankings/.env.cp`. To configure: 
* Use `cp power_rankings/.env.cp power_rankings/.env` to copy this file to the location the app 
is configured to read from. 
* Use  `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
to generate a secret key. 
* Use vim or a text editor to place this key in your .env file for `DJANGO_SECRET_KEY`. 
* You may also change any other configuration a you like (though, the rest of this guide assumes you do not).

## 'Install' postgresql

```commandline
docker pull postgres
mkdir $HOME/dev-postgres-data
docker run --name dev-postgres -p 5433:5432 -e POSTGRES_USER=postgresUser -e POSTGRES_PASSWORD=postgresPW -d -v $HOME/postgres-data/:/var/lib/postgresql/data postgres
```

Once this is running, you should have a postgresql database available locally on port 5433 with the specified credentials.
Moreover, we have made a persistent location for our postgres data to exist: `$HOME/dev-postgres-data`. Now, we just need
to set up the database our app will use. 

* `docker exec -it dev-postgres bash` to get a bash shell in the postgres container
* `psql -h localhost -U postgresUser` to get access to the database directly
* `CREATE DATABASE dev;` to create the `dev` database.

## Creating an Admin User

Follow [django's instructions](https://docs.djangoproject.com/en/1.8/intro/tutorial02/#creating-an-admin-user) for 
creating an admin user.

## Launching the App

`python power_rankings/manage.py runserver`
