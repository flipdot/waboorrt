# waboorrt

Install docker compose

    docker-compose up --build

## Development setup: gameserver

Use pipenv (`pip install pipenv`).

    cd gameserver/
    # install dependencies
    pipenv sync
    # run tests
    pipenv run nosetests
    # format code
    pipenv run black
    # check style
    pipenv run flake8