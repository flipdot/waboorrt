curl -s -X POST -H "Content-Type: application/json" -d '{"method": "health", "jsonrpc": "2.0", "id": 420, "params": {}}' http://localhost:4000/jsonrpc | jq .result

curl -s -X POST -H "Content-Type: application/json" --data-binary "@jsonrpc-testinput.txt" http://localhost:4000/jsonrpc | jq .result