# SharingSketch _- a synchronization drawing tool._
**Sharing Sketch is a real-time synchronization drawing tool, designed to collaborate with users on one canvas.**
- **Demo Site**: https://bizara.link/

<div align="center">
  <img src="https://github.com/user-attachments/assets/2e825db7-49c3-4220-80e7-7c614aba8efd" width="80%"></img>
</div>


## Features

### Join Room

- **Join Room:** Enter a new room name and join the room, or use the room list to enter an existing room.


https://github.com/user-attachments/assets/29593eee-928a-4bf1-ab65-7b7c577047a6



---

### Sketch

- **Paint Tools:** Draw with a pen or an eraser that allows you to adjust color and line width.


https://github.com/user-attachments/assets/a8133998-eab7-4eb2-9fc2-b289911082b5



---

- **Canvas Tools:** Provide undo, mirror, and selection adjustment functionalities to enhance drawing efficiency.


https://github.com/user-attachments/assets/44beef46-0ca5-4879-aacc-e69263c60926



---

- **File Tools:** Download image or export to SketchGallery for storage, as well as import image from your device to continue drawing.


https://github.com/user-attachments/assets/6f8e84d8-9e1a-4cfc-aa44-9db05512daea

---

- **Layer Tools:** Create individual layers and easily change their order.


https://github.com/user-attachments/assets/218bfdef-ab52-49a5-9905-91536cf219c7



---

### Gallery

- **Delete:** Delete images if the user is the creator, ensuring proper permissions.
- **Export:** Export image to SharingSketch for further editing.
- **Download:** Download images to your device.


https://github.com/user-attachments/assets/12d132a8-f305-4cc0-ad9e-0e010712fd26



---

## Tech Stack

- **Sharing Sketch:**
  - **Programming Language:** Python
  - **Server:** Flask(Flask-SocketIO)
  - **Client:** HTML,CSS,JavaScript(SocketIO)
  - **Database:** SQLite
- **Sketch Gallery(Repo [link](https://github.com/z50205/SketchGallery_front.git)):**
  - **Programming Language:** JavaScript
  - **Server:** Node.js,Express.js
  - **Client:** React.js
  - **Database:** SQLite
- **Deploy and Environment:**
  - **Proxy Server:** Nginx
  - **Containerization:** Docker
  - **AWS Cloud Service:** EC2

## Design Concept

### Architecture Design
- **Nginx Proxy:**  Reverse proxy to hide the specific addresses of backend containers, enhancing security and increasing flexibility.
<div align="center">
  <img src="https://github.com/user-attachments/assets/bddccf38-3857-4b35-a5f6-6fc2df72d787" width="80%"></img>
</div>


### Synchronization Canvas
- **Canvas Stack:** Use a series of SocketIO canvas element to synchronize each users and implement drawing tools.
<div align="center">
  <img src="https://github.com/user-attachments/assets/80ac7927-930a-4c23-921d-9ec65bb2d06c" width="80%"></img>
</div>


## Utilize Details

### Deploy on AWS EC2 for example:

- **1. git clone to VM/PC:**`git clone https://github.com/z50205/PSS_websocket.git`

- **2. change and add parameter**

  1. room.html(javascript):`const socket = io('http://[your ip/domain name]', { transports: ["websocket"], autoConnect: false });`
  2. \_\_init.py(python):`socketio.init_app(app, cors_allowed_origins=['http://[your ip/domain name]','http://[your ip/domain name]:8002'])`
  3. .env: add `SECRET_KEY='xxxxxxxx'`

- **3. Docker build container:** `docker build -t [imagesname] .`

- **4. Docker compose:** `docker compose up -d`

