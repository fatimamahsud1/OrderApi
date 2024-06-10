from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Test</title>
</head>
<body>
    <h1>WebSocket Client</h1>
    <ul id='messages'>
    </ul>
    <script>
        var ws = new WebSocket("ws://localhost:8001/ws");
        ws.onmessage = function(event) {
            var messages = document.getElementById('messages')
            var message = document.createElement('li')
            var content = document.createTextNode(event.data);
            message.appendChild(content);
            messages.appendChild(message);
        };
    </script>
</body>
</html>
"""

@app.get("/")
def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = "Update!"  # This should be replaced with actual data logic
        await websocket.send_text(f"Data update: {data}")
        await asyncio.sleep(1)  # Example: Send updates every second

