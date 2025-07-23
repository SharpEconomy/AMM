# AMM Controller

Proof-of-concept Django app for monitoring a Uniswap V3 liquidity pool on Polygon and comparing price with Bitmart and Coinstore.

## Setup

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in values (`ALCHEMY_URL`, `POOL_ADDRESS`, etc).
3. Run migrations and start the scheduler:
   ```bash
   python manage.py migrate
   RUN_SCHEDULER=1 python manage.py runserver
   ```
   The scheduler runs in-process and syncs prices every minute.

## Management Commands

- `python manage.py start_scheduler` – run the scheduler alone.

The dashboard is available at `/` and Django admin at `/admin/`.
