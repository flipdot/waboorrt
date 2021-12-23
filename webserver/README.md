# Webserver

    pipenv sync
    pipenv run python app.py

Visit http://localhost:8080/docs for the API explorer.

http://localhost:8080/ will serve the frontend from `static/webapp`.
Build the frontend and copy `frontend/dist` to `static/webapp`

## Frontend

Build dist:

    cd frontend
    npm i
    npm run-script build
    mv dist ../static/webapp

## Database migrations

The project uses [alembic](https://alembic.sqlalchemy.org/) to manage database migrations.
Migrate to the most recent db revision by running this command:

    alembic upgrade head
    
More information: https://alembic.sqlalchemy.org/en/latest/tutorial.html#running-our-first-migration
