# waboorrt

Install docker compose. Create a network for the bots and run compose up

    docker network create --internal gamenet
    docker-compose up --build

Gameserver interface: http://localhost:5000

## Development setup: gameserver

Use pipenv (`pip install pipenv`).

    cd gameserver/
    # install dependencies
    pipenv sync
    # run tests
    pipenv run nosetests
    # format code
    pipenv run black .
    # check style
    pipenv run flake8

Build the "pyrandom" docker image:

    cd bot-templates/python
    docker build -t localhost/bot/pyrandom .