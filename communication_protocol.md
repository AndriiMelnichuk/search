# Comunication protocol
## Task search
``` shell
curl -X POST http://localhost:5010/task -H "Content-Type: application/json" -d '{
    "jwt": "key",
    "group_id": "test id",
    "text": "title/descr",
    "assigned_to": ["test name", ...],
    "complete_before": "mm/dd/yyyy",
    "status": "todo(true/false/'')"
}'

return_type {
    "id": ["id0", ...],
    "title": ["name0", ...],
    "description": ["desc0", ...],
    "deadline": ["deadline0", ...],
    "assigned": [["member00", "member01", ...], ["member10", ...], ...],
    "status": ["todo_task0", ...]
}
```

## Group search
``` shell
curl -X POST http://localhost:5010/group -H "Content-Type: application/json" -d '{
    "jwt": "key",
    "text": "test name"
}'

return_type {
    "id": ["id0", ...],
    "name": ["name0", ...]
}
```