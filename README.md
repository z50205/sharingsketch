# SharingSketch _- a synchronization drawing tool._
**Sharing Sketch is a real-time synchronization drawing tool, designed to collaborate with users on one canvas.**
![alt text](PSS/static/Sample.png)
- **Demo Site**: https://bizara.link/

## Features

### Join Room

- **Join Room:** Enter a new room name and join the room, or use the room list to enter an existing room.
  <video controls src="./Record/Join.mp4" title="Join Room"></video>

---

### Sketch

- **Paint Tools:** Draw with a pen or an eraser that allows you to adjust color and line width.
  <video controls src="./Record/Paint.mp4" title="Paint Tools"></video>

---

- **Canvas Tools:** Provide undo, mirror, and selection adjustment functionalities to enhance drawing efficiency.
  <video controls src="./Record/Canvas.mp4" title="Canvas Tools"></video>

---

- **File Tools:** Download image or export to SketchGallery for storage, as well as import image from your device to continue drawing.
  <video controls src="./Record/File.mp4" title="File Tools"></video>

---

- **Layer Tools:** Create individual layers and easily change their order.
  <video controls src="./Record/Layer.mp4" title="Layer Tools"></video>

---

### Gallery

- **Delete:** Delete images if the user is the creator, ensuring proper permissions.
- **Export:** Export image to SharingSketch for further editing.
- **Download:** Download images to your device.
  <video controls src="./Record/Gallery.mp4" title="Gallery"></video>

---

## Tech Stack

- **Sharing Sketch:**
  - **Programming Language:** Python
  - **Server:** Flask(Flask-SocketIO)
  - **Client:** HTML,CSS,JavaScript(SocketIO)
  - **Database:** SQLite
- **Sketch Gallery(Rep link):**
  - **Programming Language:** JavaScript
  - **Server:** Node.js,Express.js
  - **Client:** React.js
  - **Database:** SQLite
- **Deploy and Environment:**
  - **Proxy Server:** Nginx
  - **Containerization:** Docker
  - **AWS Cloud Service:** EC2

## Design Concept

### Synchronization Canvas
- **Canvas Stack:** Use a series of SocketIO canvas element to synchronize each users and implement drawing tools.
-  ![SharingSketch_intro3](https://github.com/user-attachments/assets/80ac7927-930a-4c23-921d-9ec65bb2d06c)

### Architecture Design
- **Nginx Proxy:**  Reverse proxy to hide the specific addresses of backend containers, enhancing security and increasing flexibility.
-  ![alt text](PSS/static/Architecture.gif)

## Utilize Details

### Deploy on AWS EC2 for example:

- **1. git clone to VM/PC:**`git clone https://github.com/z50205/PSS_websocket.git`

- **2. change and add parameter**

  1. room.html(javascript):`const socket = io('http://[your ip/domain name]', { transports: ["websocket"], autoConnect: false });`
  2. \_\_init.py(python):`socketio.init_app(app, cors_allowed_origins=['http://[your ip/domain name]','http://[your ip/domain name]:8002'])`
  3. .env: add `SECRET_KEY='xxxxxxxx'`

- **3. Docker build container:** `docker build -t [imagesname] .`

- **4. Docker compose:** `docker compose up -d`

