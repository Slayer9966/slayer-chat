from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Websocket Demo</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <style>
    body {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
        background-color: azure;
               font-family: 'Roboto', sans-serif;

    }

    .chat-container {
        height: 400px;
        background-color: #128C7E;
        width: 500px;
        position: relative;
        overflow-y: auto;
        padding: 20px;
    }

   .input-group {
            margin-top:0px;
            z-index: 99;
            bottom: 0;
            left: 0;
            width: 100%;
            display: flex;
            padding: 10px;
            background-color: #fff;
            border-right: black 0.5px solid;
            border-left: black 0.5px solid;
            border-bottom: black 0.5px solid;
        }

    .message-input {
        flex: 1;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        margin-right: 10px;
    }

    .send-button {
        width: 70px;
        height: 50px;
        border-radius: 50%;
        border: none;
        background-color: #128C7E;
        color: white;
        font-size: 20px;
        cursor: pointer;
    }

    /* CSS for message styling */
    .message-container {
        margin-bottom: 10px;
    }

    .received-message {
        text-align: right;
        background-color: #f0f0f0;
        padding: 8px;
        border-radius: 10px;
        max-width: 70%;
        margin-left: auto;
    }

    .sent-message {
        text-align: left;
        background-color: #dcf8c6;
        padding: 8px;
        border-radius: 10px;
        max-width: 70%;
        margin-right: auto;
    }
    </style>
</head>

<body>

<div style="text-align:center; background-color:lightgreen; overflow:hidden;border-radius:10px;">
<h1 >Slayer Chat </h1>
<div class="chat-container mt-5">
    <div id='messages'>
        <!-- Messages will be displayed here -->
    </div>
   
</div>
 <div class="input-group">
        <input type="text" class="form-control message-input" id="messageText" placeholder="Type a message..." autocomplete="off"/>
        <button class="btn btn-primary send-button" onclick="sendMessage()">Send</button>
    </div>
</div>

<script>
var name = prompt("Please enter your name:");

var ws = new WebSocket(`ws://127.0.0.1:8000/ws/?name=${name}`);
ws.onmessage = function(event) {
console.log("sent")
  var myDiv = document.getElementsByClassName('chat-container');
  myDiv[0].scrollTop = myDiv.scrollHeight;

    var messages = document.getElementById('messages');
    var message = document.createElement('div');
    var content = document.createTextNode(event.data);
    message.appendChild(content);

    // Check if the message was sent by the current client
     if (!event.data.includes('you :')) { 
        // Message was sent by others
        message.className = "message-container received-message";
        messages.appendChild(message);  
    } else {
        // Message was sent by current client
        message.className = "message-container sent-message";
        messages.appendChild(message);  
    }
};

function sendMessage() {
    var input = document.getElementById("messageText");
    ws.send(input.value);
    input.value = '';
}
</script>
</body>
</html>
"""

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, name: str):
        await websocket.accept()
        self.active_connections[websocket] = name

    def disconnect(self, websocket: WebSocket):
        del self.active_connections[websocket]
    
    async def send_personal_message(self, message: str, sender_name: str, recipient_websocket: WebSocket, sender_websocket: WebSocket, recipient_name: str):
        await recipient_websocket.send_text(f"Personal messege from {sender_name}: {message}")
        await sender_websocket.send_text(f"Personal messege for {recipient_name}: {message}")



    async def broadcast(self, message: str, sender: WebSocket):
        sender_name = self.active_connections[sender]
        for connection, name in self.active_connections.items():
            if connection != sender:
                await connection.send_text(f"{sender_name}: {message}")
            else:
                await connection.send_text(f"you : {message}")

manager = ConnectionManager()

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket, name: str):
    await manager.connect(websocket, name)
    
    try:
        while True:
            data = await websocket.receive_text()
            if(data=="GoodBye"):
                 await websocket.close()
                 break
            
            if data.startswith("@"):
                # Extract recipient name and message
                recipient_name, message = data.split(" ", 1)
                recipient_name = recipient_name[1:]  # Remove "@"
                # Find the recipient WebSocket connection
                recipient_connection = None
                for connection, connection_name in manager.active_connections.items():
                    if connection_name == recipient_name:
                        recipient_connection = connection
                        break
                if recipient_connection:
                    await manager.send_personal_message(message, name, recipient_connection, websocket, recipient_name)
                else:
                    await manager.send_personal_message("User not found", name, websocket, websocket, recipient_name)
            else:
                await manager.broadcast(data, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
