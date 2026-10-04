# Smart Power Usage Tracker

Smart Power Usage Tracker is a Django-based household electricity tracking application designed to separate actual meter-based usage from estimated appliance usage. It helps households log homes, appliances, meter readings, and tariff-driven cost estimates, while surfacing rule-based energy insights and a simple dashboard.

## Features implemented

- User registration and login
- Multi-home support per user
- Appliance creation with power, runtime, and quantity assumptions
- Appliance kWh estimation based on the formula: `(power_watts × hours_per_day × days × quantity) / 1000`
- Manual and CSV-based meter reading entry
- Actual household usage computed from cumulative meter sequences
- Tariff configuration and deterministic tier-based pricing
- Dashboard with summary cards and Chart.js charts
- Rule-based energy insights
- REST API with authentication and ownership filtering

## Architecture

This project follows a modular Django app structure:

- `accounts` – authentication and profile pages
- `homes` – household management
- `appliances` – appliance records and usage assumptions
- `electricity` – meter readings and CSV import flow
- `billing` – tariff and rate configuration
- `analytics` – summary calculations and dashboard data
- `insights` – deterministic recommendations
- `api` – JSON endpoints for the app and future frontend integration

## Local setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   . .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a local `.env` file based on `.env.example`.
4. Create or confirm the PostgreSQL database `smart_power` exists for the current Linux user.
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the development server:
   ```bash
   python manage.py runserver 127.0.0.1:8000
   ```

## Default routes

- `/accounts/login/`
- `/accounts/register/`
- `/dashboard/`
- `/homes/`
- `/appliances/`
- `/readings/`
- `/billing/`
- `/analytics/`
- `/insights/`
- `/api/auth/`

## Testing

Run:

```bash
python manage.py test
```

## Relationship to future AI/ML

The system captures clean historical usage and tariff data in a way that can support later forecasting, anomaly detection, and AI explanations without restructuring the core model. The current MVP does not implement ML or external provider integration.
