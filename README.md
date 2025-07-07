# Issue Insight Tracker
Issue Insight is used to track and manage Issues. 

## Setup

### VIA Docker

Pre Requsite
* docker 
* docker compose

Before starting the docker compose, setup the following `.env` files. 
In both `frontend` and `backend`. You will have a file called `.env.example` (An Example ENV). It almost contains all the necessary env. 

But, you need to configure `Clerk` API keys inorder to run. The `Authentication` is handled via [clerk](https://clerk.com/)

SET your clerk's both public key (starts with `pk_`), secret key (starts with `sk`). Actually, Frontend will not use clerk's secret key, It is configured for future purpose for `Svelte Server Side` if needed.

An Example `.env` --> frontend/
```
PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_35OB6Vdl2MdFAvikJ8n1MW8S3gK0ZdtDQ4A9yf3B1I
CLERK_SECRET_KEY=sk_live_70842963715849326017458392016472839105724816
```

Again, SET your clerk's private key (starts with `sk`) in the backend env.

An Example `.env` --> backend/
```
CLERK_SECRET_KEY=sk_live_70842963715849326017458392016472839105724816
```

Now all set, Just run
```
docker compose up
```

* Your Frontend server will be exposed at the port `4173`
* Your Backend Server will be exposed at the port `8181`