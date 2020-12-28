curl -s -X POST -H "Content-Type: application/json" -d '{"method": "hello", "jsonrpc": "2.0", "id": 420, "params": {}}' http://localhost:4000/jsonrpc | jq .result

curl -s -X POST -H "Content-Type: application/json" -d '{"method": "next_action", "jsonrpc": "2.0", "id": 420, "params": {"game_state": "stuff", "your_name": "Hans"}}' http://localhost:4000/jsonrpc | jq .result