# 💬 Slayer Chat - Real-time WebSocket Chat
**Slayer Chat** is a real-time chat application built with **FastAPI** and **WebSockets**. It features a WhatsApp-inspired UI with support for both group messaging and private messages between users.
---
## 🚀 Features
### 💬 Real-time Messaging
- Instant message delivery using WebSockets
- WhatsApp-style chat interface with message bubbles
- Auto-scroll for new messages
- Connection status management
### 👥 Multi-user Support
- Multiple users can join the chat simultaneously
- User identification with custom names
- Broadcast messages to all connected users
- Private messaging with `@username` format
---
## 🛠️ Tech Stack
- **Backend:** FastAPI (Python)
- **WebSockets:** Native FastAPI WebSocket support
- **Frontend:** HTML5, CSS3, JavaScript
- **Styling:** Bootstrap 5
- **Server:** Uvicorn ASGI server
---
---
## ⚙️ Setup Instructions
### ✅ Clone the Repo
```bash
git clone https://github.com/Slayer9966/slayer-chat.git
cd slayer-chat
```
---
### 🐍 Python Environment Setup
```bash
python -m venv venv
venv\Scripts\activate       # For Windows
# or
source venv/bin/activate    # For macOS/Linux
pip install fastapi uvicorn websockets
```
---
### 🚀 Run the Application
```bash
python main.py
# or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
This will start the server at:
**http://localhost:8000**
---
## 📱 How to Use
### 🔗 Join the Chat
1. Open your browser and navigate to `http://localhost:8000`
2. Enter your name when prompted
3. Start chatting with other connected users
### 💬 Send Messages
- **Group Message:** Simply type your message and hit Send
- **Private Message:** Use `@username your message` format
### 🚪 Leave the Chat
- Type `GoodBye` to disconnect gracefully
- Or simply close the browser tab
---
## 📌 Notes
- This is a demo application for learning WebSocket implementation
- No message persistence - messages are lost on server restart
- No authentication or user management system
- Designed for local network or development use
---
## 📜 License
Licensed under the [MIT License](LICENSE) — use, modify, and distribute freely.
---
## 🙋‍♂️ Author
**Syed Muhammad Faizan Ali**  
📍 Islamabad, Pakistan  
📧 faizandev666@gmail.com  
🔗 [GitHub](https://github.com/Slayer9966) | [LinkedIn](https://www.linkedin.com/in/faizan-ali-7b4275297/)
📢 If you find this project helpful or use it in your work, please consider giving it a ⭐ or letting me know via email or GitHub issues!
