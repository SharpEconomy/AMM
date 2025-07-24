# AMM Controller

Proof-of-concept Django app for monitoring a Uniswap V3 liquidity pool on Polygon and comparing price with Bitmart and Coinstore.

## Setup

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file and set the required variables (`ALCHEMY_URL`, `POOL_ADDRESS`, etc).
   Without a valid `ALCHEMY_URL` or outbound internet access the live prices will
   show as `N/A`.
3. Start the development server. Pending migrations run automatically (set
   `AUTO_MIGRATE=0` to disable):
   ```bash
   RUN_SCHEDULER=1 python manage.py runserver
   ```
   The scheduler runs in-process and syncs prices every minute by default.
   Set `SYNC_INTERVAL_SECONDS` to change the interval.
4. Before deploying, collect static files:
   ```bash
   python manage.py collectstatic --noinput
   ```

## Management Commands

- `python manage.py start_scheduler` – run the scheduler alone.

The dashboard is available at `/` and provides a single-page interface for all
features. Bitmart and Coinstore prices may show as `N/A` if their APIs are
unreachable. Uniswap data likewise requires `ALCHEMY_URL` to be set correctly.

Authentication has been removed; anyone with access to the app URL can view the
dashboard.


## Deploying to Render

The included `render.yaml` defines a free web service. Create a new **Web Service**
in Render using this repository and configure the following environment
variables in the Render dashboard:

- `DJANGO_SECRET_KEY` – your Django secret key
- `ALCHEMY_URL` – Polygon RPC URL from Alchemy
- `POOL_ADDRESS` – Uniswap V3 pool address
- `PRIVATE_KEY` – optional wallet key for write actions
- `PRICE_THRESHOLD` – optional percentage threshold (default `1.0`)
- `SYNC_INTERVAL_SECONDS` – how often to fetch prices (default `60`)
- `RUN_SCHEDULER` – set to `1` to start the APScheduler in the web process
- `ALLOWED_HOSTS` – comma-separated list of allowed hosts (optional)
- `RENDER_EXTERNAL_HOSTNAME` will be added automatically if provided by Render

Render will automatically install requirements, run migrations and collect
static files via the `preDeployCommand`, and start the app with Gunicorn.
