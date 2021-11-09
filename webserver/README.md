# Webserver

    pipenv sync
    pipenv run flask run -p 8080

Visit http://localhost:8080/api

http://localhost:8080/ will serve the frontend from `static/webapp`.
Build the frontend and copy `frontend/dist` to `static/webapp`

## Frontend

Build dist:

    cd frontend
    npm i
    npm run-script build
    mv dist ../static/webapp
