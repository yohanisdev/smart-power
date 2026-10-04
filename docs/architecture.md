# Architecture

The project uses a layered Django structure with clear separation between presentation, business logic, and data access.

## Layering

- Presentation: Django templates, HTML, CSS, JavaScript, Chart.js
- API: Django REST Framework endpoints under `api/`
- Business logic: service modules in `billing/services.py`, `analytics/services.py`, and `insights/services.py`
- Data access: Django ORM models for homes, appliances, readings, tariffs, and insights

## App responsibilities

- `accounts`: authentication and profile pages
- `homes`: household ownership and grouping
- `appliances`: electric devices and usage assumptions
- `electricity`: actual meter readings and CSV import
- `billing`: tariff definitions and deterministic cost calculations
- `analytics`: calculated summaries and dashboard values
- `insights`: rule-based recommendations
- `api`: JSON interfaces and permissions

## Important design principle

Actual household consumption and estimated appliance consumption are intentionally separated in the UI and business logic. The dashboard labels the appliance values as estimates and keeps actual metered values distinct.
