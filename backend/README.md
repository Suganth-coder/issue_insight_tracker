# Backend(FastAPI)
Backend System is created using 
* Python(FastAPI)
* PostgreSQL
* APScheduler(Background Task)
* SQLAlchemy (ORM)
## Setup

Pre Requisite
* [Poetry](https://python-poetry.org/)

Poetry is used to manage all the dependencies easily

cd into the backend folder `backend/` and RUN,
```sh
poetry install
```

This will create install all the dependencies. Now Before running the web server, you need to set `.env`

Change `.env.example` to `.env` and set the `CLERK_SECRET_KEY`

To run the `Web Server`,
```sh
poetry run python3 main.py
```

To run the `Scheduler`,
```sh
poetry run python3 worker.py
```

## Folder Structures

* Schemas are in the folder `schemas/`
* API Routes are in the folder `routers/`
* Library files are in the folder `library/`
* Authentication files are in the folder `library/authentication`
* Issue Management files are in the folder `library/issues`

## Request Flow

* Request will reach the specific routes `routers/`
* Then it will pass to `ClerkAuthentication.authorize` custom created decorator for handing the clerk authorization part.
* Check if the Request is Authenticated, then pass to function else return `403 UnAuthorized`

### WebSockets

Websockets are handled by `websocket_endpoint` in `routers/app.py`.Messages to the connected clients will send via [routers/websocket.py](routers.websocket.py)