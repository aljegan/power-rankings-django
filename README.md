# power-rankings-django

This is an example project demonstrating how to set up a simple
power rankings application using the Django framework. For a
database, we will use postgresql (and docker). To install dependencies,
first confirm that you are using a Python 3.6 installation with `python -V`. Then, 
`python -m venv env && source env/bin/activate`, then (from the new shell) 
`python -m pip install requirements.txt`


## 'Install' postgresql

These instructions are for a mac with docker desktop already installed.

```commandline
docker pull postgres
mkdir $HOME/dev-postgres-data
docker run --name dev-postgres -p 5433:5432 -e POSTGRES_USER=postgresUser -e POSTGRES_PASSWORD=postgresPW -d -v $HOME/postgres-data/:/var/lib/postgresql/data postgres
```

Once this is running, you should have a postgresql database running locally on port 5433 with the specified credentials.
Moreover, we have made a persistent location for postgres' data to exist: `$HOME/dev-postgres-data`. Now, we just need
to set up the database our app will use. 

* `docker exec -it dev-postgres bash` to get a bash shell in the postgres container
* `psql -h localhost -U postgresUser` to get access to the database directly
* `CREATE DATABASE dev;` to create the `dev` database.