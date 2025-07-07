# Issue Insight Tracker
Issue Insight is used to track and manage Issues. 
![issue_insight_tracker](images/issue_tracker.png)

## Setup

### via Docker

Pre Requisite
* [docker](https://www.docker.com/)
* [docker compose](https://docs.docker.com/compose/)

Before starting the docker compose, setup the following `.env` files in both `frontend/` and `backend/` folders. You will have a file called `.env.example` (An Example ENV). It almost contains all the necessary env. 

But, you need to configure `Clerk` API keys in order to run. The `Authentication` is handled by [clerk](https://clerk.com/)

SET both clerk's public key (starts with `pk_`), secret key (starts with `sk`) like below. Actually, Frontend will not use clerk's secret key, It is configured for future purpose for `Svelte Server Side` if needed.

An Example `.env` --> frontend/
```env
PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_35OB6Vdl2MdFAvikJ8n1MW8S3gK0ZdtDQ4A9yf3B1I
CLERK_SECRET_KEY=sk_live_70842963715849326017458392016472839105724816
```

Again, SET your clerk's private key (starts with `sk`) in the backend env.

An Example `.env` --> backend/
```env
CLERK_SECRET_KEY=sk_live_70842963715849326017458392016472839105724816
```

Now all set, Just run
```sh
docker compose up
```

* Your Frontend server will be exposed at the port `4173`
* Your Backend Server will be exposed at the port `8181`

## via Local

### Frontend
Refer this [Frontend README File](frontend/README.md)

### Backend
Refer this [Backend README File](backend/README.md)

## Architecture 

Used Components

* Frontend: Svelte

* Backend: FastAPI (Python)
* Database: PostgreSQL
* ORM: SQLAlchemy
* Scheduler: APScheduler
* S3 Storage: MinIO 
* Authentication (OAuth2): clerk

#### How secure the system is?
* Frontend ---> Send Request to the clerk and get authenticated
* After successful authentication, Frontend SDK `svelte-clerk` will receive Session Token
* This Session Token is passed to the backend in `Authorization: Bearer <Session Token>` header
* Backend will do the `authorization` part. It will verify with the clerk, using `CLERK_SECRET_KEY`
* If authorized, let in else not. After successful authorization, if the user is new, `User Role` will be created for them

Only the authorized users able to access the routes.

`Backend API Docs Link`
After Running the backend (issue-web service in docker or locally) visit `http://localhost:8181/docs`  

## Scheduler 
This is the Scheduler File `backend/Worker.py`. It will aggregate the issue counts based on status tag into `daily_stats` table for every 30 mins

## Bonus Task
Implemented Pydantic-v2's `BeforeValidator` and `AfterValidator` in 
[backend/schemas/issue_schema.py](backend/schemas/issue_schema.py)

