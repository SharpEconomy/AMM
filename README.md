# AMM Controller

Proof-of-concept Django app for monitoring a Uniswap V3 liquidity pool on Polygon and comparing price with Bitmart and Coinstore.

## Setup

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file and set the required variables (`ALCHEMY_URL`, `POOL_ADDRESS`, etc).
3. Run migrations and start the scheduler:
   ```bash
   python manage.py migrate
   RUN_SCHEDULER=1 python manage.py runserver
   ```
   The scheduler runs in-process and syncs prices every minute.

## Management Commands

- `python manage.py start_scheduler` – run the scheduler alone.

The dashboard is available at `/` and Django admin at `/admin/`.

## Deploying to Render

The included `render.yaml` defines a free web service. Create a new **Web Service**
in Render using this repository and configure the following environment
variables in the Render dashboard:

- `DJANGO_SECRET_KEY` – your Django secret key
- `ALCHEMY_URL` – Polygon RPC URL from Alchemy
- `POOL_ADDRESS` – Uniswap V3 pool address
- `PRIVATE_KEY` – optional wallet key for write actions
- `PRICE_THRESHOLD` – optional percentage threshold (default `1.0`)
- `RUN_SCHEDULER` – set to `1` to start the APScheduler in the web process
- `ALLOWED_HOSTS` – comma-separated list of allowed hosts (optional)
- `RENDER_EXTERNAL_HOSTNAME` will be added automatically if provided by Render

Render will automatically install requirements, run migrations via the
`preDeployCommand`, and start the app with Gunicorn.
