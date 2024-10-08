

## Video Overview


https://github.com/user-attachments/assets/fe85d54f-3b10-4c8c-8792-af09bfd53c03



### Django Environment Variables create the .env inside django project directory add this variable

---

- ` DEBUG`: Debug mode. If on, will display details of error pages. If your app raises an exception when DEBUG is on, will display a detailed traceback, including a lot of metadata about the environment, such as all the currently defined Django settinngs . Never deploy a site into production with DEBUG turned on.
- ` SECRET_KEY`: The secret key to use for cryptographic operations should be set to a unique, unpredictable value. Never deploy a site into production with the default secret key.
- ` DB_NAME`: The NAME of the db to use
- ` DB_USER`: The URSERNAME of the database to use
- ` DB_PASS`: The PASSWORD of the database to use
- ` DB_PORT`: The PORT of the database to use ( #defined in the postgres configration docker-compose.yml )
- ` DB_HOST`: The HOST of the database to use ( #service name of postgres defined in the postgres configration docker-compose.yml )

### warn before run

- `create an env directory  crate 2 files 1 .env which is for the docker project enviornment 2 .postgres_env for storing creadential of the postgres databse `

## in .env create a 3 varaibles

- ` APPLICATION_ID the applicatio id for dockerapplication`
- `APPLICATION_MODE  use developement on developement use production on production mode `
- `APPLICATION_DATABASE name the type of database `

## in .postgres_env

- `POSTGRES_DB  db name new db  of postgres for the django application`
- `POSTGRES_USER name the username  you want use`
- `POSTGRES_PASSWORD provide the password you want`

### Run Docker Compose To Run The Application

---

- `docker-compose --project-name=projectnameyouwant -f docker-compose.yml up` - Run the project environment.
- `docker-compose --project-name=projectnameyouwant -f docker-compose.yml up --build -d` - Build the project environment and run it.
- ` docker-compose --project-name=projectnameyouwant -f docker-compose.yml -f docker-compose.production.yml up` - Run the production environment.
- `
` - Build the production environment and run it.

### Dockerized Django Docker Commands

---

- ` docker-compose --project-name=projectnameyouwant -f docker-compose.yml down --remove-orphans` - Stop all containers in the compose file and delete orphaned containers associated with them.
- `docker network create supernet` - Create network 'supernet' if it doesn't exists.
- `docker system prune -af` - Remove all stopped containers, networks, volumes, and images.
- `docker network create supernet` - Create the network manually.
- `docker logs -f --tail 100 projectnameyouwant-django-1` - Display django consol logs.
- `docker exec -it projectnameyouwant-django-1 sh` - Access django shell.

### Backup & Restore Database

---

- `docker exec -t PostgreSQL pg_dumpall -c -U DockerizedDjangoUser > dump/dump_latest.sql` - Backup
- `cat dump/dump_latest.sql | docker exec -i PostgreSQL psql -U DockerizedDjangoUser` - Restore
