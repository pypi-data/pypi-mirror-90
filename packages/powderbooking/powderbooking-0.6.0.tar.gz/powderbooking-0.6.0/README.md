# powderbooking-database

Database model for the Powderbooking application

## How to use

This database model is pushed to pypi to make it available for all microservices.

This package uses [Poetry](https://python-poetry.org/) to maintain dependencies and to push to pypi.

## Environmental variables

To use this package to create the database connection, the following environmental variables need to be set.

| name  | optional  | description |
|---|---|---|
|PROJECT_NAME   | false   | The name of the project, that is used by kubernetes to indicate service port and host.  |
|POSTGRESQL_USER   | false   | the username  |
|POSTGRESQL_PASSWORD   | false   | the password  |
|{PROJECT_NAME}_POSTGRESQL_SERVICE_HOST   | false   | host of postgresql  |
|{PROJECT_NAME}_POSTGRESQL_SERVICE_PORT   | false   | port of postgresql  |
|POSTGRESQL_DATABASE   | false   | the database that is used  |

## Development

### Initialize an example database
To initialize a database with the schema, I have created an example app. To use it, follow the steps below:

1. Check the prerequisites of the powderbooking group (e.g. have Docker, Poetry installed)
2. Install the package. In the terminal, execute at the root of this project:    
   `poetry install`
3. Create a `db.env` in the `compose` folder, using the `db.env.template`.
4. Start the database. In the terminal, execute at `./compose`:   
   `docker-compose up -d`
5. Edit or add the run configuration in your IDE for `./compose/app.py` to use the `db.env`
6. Run `./compose/app.py` in your IDE
7. You should now be able to inspect the database at the url provided by the script.

### Cleanup
To remove the database - in the terminal, execute at `./compose`:   
`docker-compose down --remove-orphans --volumes`