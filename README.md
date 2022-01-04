Dump games from API:

    curl 'https://waboorrt.flipdot.org/api/games' > api/games/index.html
    cat api/games/index.html | jq -r '.[] | .id' > ids.lst
    parallel -j100 "[[ -f '{}' ]] || (curl -sX 'GET' 'https://waboorrt.flipdot.org/api/games/{}' -H 'accept: application/json' -o 'api/games/{}'; echo -en '\033[100D{#}/$l')" < ids.lst
    
(index.html is actually json, but giving it the name "index.html" will
allow GitHub pages to return it when opening `/api/games`)