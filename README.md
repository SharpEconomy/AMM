# AMM Controller

Proof-of-concept Django app for monitoring a Uniswap V3 liquidity pool on Polygon and comparing price with Bitmart and Coinstore.

## Setup

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file and set the required variables (`POOL_ADDRESS`, etc).
   The app queries the Uniswap V3 API directly and no RPC provider is needed.
   Without network access the live prices will show as `N/A`.
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
unreachable. Uniswap data is retrieved from the public API and requires
outbound network access.

Authentication has been removed; anyone with access to the app URL can view the
dashboard.

## API Endpoints

- `/api/latest/` – most recent price snapshot
- `/api/opportunities/` – recent arbitrage opportunities
- `/api/bitmart_price/` – latest Bitmart SHARP/USDT price
- `/api/coinstore_price/` – latest Coinstore SHARP/USDT price

## Deploying to Render

The included `render.yaml` defines a free web service. Create a new **Web Service**
in Render using this repository and configure the following environment
variables in the Render dashboard:

- `DJANGO_SECRET_KEY` – your Django secret key
- `POOL_ADDRESS` – Uniswap V3 pool address
- `UNISWAP_API_URL` – optional GraphQL endpoint override
- `OTP_SECRET` – base32 secret for Microsoft Authenticator login
- `PRIVATE_KEY` – optional wallet key for write actions
- `PRICE_THRESHOLD` – optional percentage threshold (default `1.0`)
- `SYNC_INTERVAL_SECONDS` – how often to fetch prices (default `60`)
- `RUN_SCHEDULER` – set to `1` to start the APScheduler in the web process
- `OTP_SECRET` – base32 secret for TOTP login
- `ALLOWED_HOSTS` – comma-separated list of allowed hosts (optional)
- `RENDER_EXTERNAL_HOSTNAME` will be added automatically if provided by Render

Render will automatically install requirements, run migrations and collect
static files via the `preDeployCommand`, and start the app with Gunicorn.
