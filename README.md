# power-rankings-django

This is an example project demonstrating how to set up a simple
power rankings application using the Django framework. For a
database, we will use postgresql (and docker).

## 'Install' postgresql

These instructions are for a mac with docker desktop already installed.

```commandline
docker pull postgres
mkdir $HOME/dev-postgres-data
docker run --name dev-postgres -p 5433:5432 -v $HOME/postgres-data/:/var/lib/postgresql/data -e POSTGRES_USER=postgresUser -e POSTGRES_PASSWORD=postgresPW -e POSTGRES_DB=postgresDB -d postgres
```

Once this is running, you should have a postgresql database running locally on port 5433 with the specified credentials.
Moreover, we have made a persistent location for postgres' data to exist: `$HOME/dev-postgres-data`.