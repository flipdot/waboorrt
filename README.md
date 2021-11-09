# waboorrt

Install docker compose. Create a network for the bots and run compose up

    docker network create --internal gamenet
    docker-compose up --build

WebUI: http://localhost
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
    docker build -t localhost/bot/$(printf %s "pyrandom" | sha256sum | head -c 32) .
    
## gitserver: adding new accounts

    docker-compose exec gitserver newbot username python "ssh-rsa AAAAB...."
    git clone ssh://username@localhost:2222/git/username.git
