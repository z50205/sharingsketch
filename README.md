# Sharing Sketch *- a synchronization drawing tool.*
**Demo Site: http://13.112.29.121/**

## Website Introduction
>* #### Project Overview:
>     This is a website tool can synchronize room members' canvases by using flask, javascript, socketIO(websocket).

>* #### Key Features:
>   **1. Synchronization canvas, drawing tools features refer to the diagram below.** *- using javascript, Flask-SocketIO*  
>
>      <img width="400" alt="SharingSketch_intro2" src="https://github.com/user-attachments/assets/6329dfbb-e758-499b-b799-13869621eed4">
>  
>   **2. Register page, Login page** *- using Flask-WTF, Flask-Login*  
>      *(Test account:username:123;password:123)*
>    
>      <img width="400" alt="SharingSketch_intro1" src="https://github.com/user-attachments/assets/81b6d210-cda0-42ed-b20a-e4a3e72917cc">
>  
## Design Concept
> ![SharingSketch_intro3](https://github.com/user-attachments/assets/80ac7927-930a-4c23-921d-9ec65bb2d06c)
## Utilize Details
>* #### Deploy:
>    **1. git clone to VM/PC:**`git clone https://github.com/z50205/PSS_websocket.git`
>
>    **2. change and add parameter**
>
>      1. room.html(javascript):`const socket = io('http://[ip]', { transports: ["websocket"], autoConnect: false });`
>     
>      2. __init.py(python):`socketio.init_app(app, cors_allowed_origins=['http://[ip]','http://[ip]:8002','http://127.0.0.1:5000'])`
>     
>      3. .env: add `SECRET_KEY='xxxxxxxx'`
>
>    **3. Docker build container:** `docker build -t [imagesname] .`
>
>    **4. Docker compose:** `docker compose up -d`
