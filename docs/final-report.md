# Final project report

## 1. Executive summary

Smart Power Usage Tracker is a Django-based household electricity tracking application created to help users separate actual household meter usage from estimated appliance consumption. It includes account management, home and appliance tracking, meter reading entry, CSV import, deterministic tariff calculations, a dashboard, and API endpoints for future frontend expansion.

## 2. Problem statement

Households often need a clear view of how much electricity is consumed in reality versus how much their appliances are estimated to use. Without that distinction, it is easy to misread energy usage trends and cost estimates. This project addresses that by keeping actual and estimated values separate and labeling them clearly.

## 3. Project objectives

- Create a working Django application that supports basic household electricity tracking
- Keep actual meter data separate from estimated appliance data
- Provide deterministic cost calculation via configurable tariff tiers
- Deliver a responsive dashboard and rule-based insights
- Provide a clean API for future frontend or AI features

## 4. Technology stack

The implementation uses:

- Python
- Django
- Django REST Framework
- PostgreSQL
- Chart.js via Django templates
- HTML/CSS/JavaScript
- Python-dotenv for environment configuration
- WhiteNoise for static file serving in local development

## 5. Architecture

The app is organized into modular apps, each with a focused responsibility. The core flow is:

- User authentication and profile access
- Home management
- Appliance creation and usage assumptions
- Meter readings and imports
- Tariff configuration and cost estimation
- Analytics and dashboard summaries
- Rule-based insights
- API access with ownership checks

## 6. Database design

The main models are:

- `Home`
- `Appliance`
- `MeterReading`
- `Tariff`
- `TariffTier`
- `Insight`

The data model keeps user-owned household information isolated, with each home linked to a user. Appliance and meter data belong to a specific home, which keeps user data separate and supports ownership filtering in the API and UI.

## 7. Backend implementation

The backend was implemented using Django apps and service modules.

- `accounts` handles login, logout, and registration pages.
- `homes` manages household records.
- `appliances` stores device assumptions and estimation logic.
- `electricity` stores actual meter readings and handles CSV import validation.
- `billing` stores tariff definitions and pricing logic.
- `analytics` calculates summary values and dashboard data.
- `insights` creates deterministic recommendations using rules.
- `api` exposes JSON endpoints protected by authentication and per-user filtering.

## 8. Frontend implementation

The frontend uses Django templates with a lightweight modern layout and Chart.js visualizations.

Included pages:

- login
- registration
- profile
- home list and detail
- appliance list and form
- meter reading list and form
- billing overview
- analytics overview
- dashboard
- insights

The dashboard clearly labels actual household consumption and estimated appliance consumption separately.

## 9. Electricity calculations

### Appliance estimate
The appliance estimate uses:

`kWh = (power_watts × hours_per_day × days × quantity) / 1000`

### Meter consumption
The project calculates actual usage by comparing sequential cumulative meter readings and rejecting invalid sequences where a later reading is lower than a previous one.

### Tariff calculation
The tariff engine is deterministic and uses configured `TariffTier` rows ordered by minimum usage, then calculates the exact usage band for each tier.

## 10. Security

Security measures implemented include:

- Django authentication system
- password hashing through Django defaults
- protected API endpoints with authentication
- ownership filtering for homes, appliances, readings, and insights
- model validation for invalid or negative values
- environment variables for secrets and database configuration

## 11. Testing

The project includes automated tests for core behavior.

Actual test results:

- 11 tests ran
- all tests passed

Test categories include:

- appliance estimation
- tariff calculation
- meter validation
- API access and auth
- home creation

## 12. CSV import

CSV import supports a simple `date,kwh` format and validates:

- required `date` and `kwh` columns
- valid date values
- numeric kWh input
- non-negative readings

Invalid rows are rejected instead of silently inserted into the database.

## 13. AI/ML readiness

The application includes extension points for future forecasting and analytics, but the MVP does not implement machine learning or AI predictions. The data model and calculation services are structured to support later tasks such as:

- historical forecasting
- anomaly detection
- cost forecasting
- AI explanations driven by structured analytics output

## 14. EEU integration

No actual EEU or utility-provider integration was implemented. The project is intentionally integration-ready but not dependent on external utility access. The architecture prepares for future official integrations by normalizing external data into the internal meter-reading model.

## 15. Deployment

The project is runnable as a local Django application and can be deployed with a standard PostgreSQL + Gunicorn/Nginx setup. Sensitive configuration is expected to remain in environment variables, not in source control.

## 16. Limitations

- This is an MVP and not a professional-grade utility billing system.
- Rules-based insights are deterministic and intentionally simple.
- No live smart meter or utility API is connected.
- The frontend remains template-based and does not yet use React.

## 17. Future improvements

- smart-meter integration
- authorized utility API integration
- ML forecasting and anomaly detection
- AI-generated explanations of electricity trends
- mobile app or progressive web app
- notifications and alerting

## 18. Development summary

The project was implemented in phases, starting with repository inspection and project initialization, followed by foundational Django configuration, account and home management, appliance models, meter ingestion, tariff logic, analytics, dashboard, API work, and final documentation.

## 19. File and module overview

Key project files:

- `config/settings.py` – Django configuration and environment settings
- `config/urls.py` – route wiring
- `homes/models.py` – home ownership model
- `appliances/models.py` – appliance model
- `electricity/models.py` – meter readings
- `billing/models.py` – tariffs and tiers
- `analytics/services.py` – usage calculations
- `insights/services.py` – rules-based recommendations
- `api/serializers.py` – JSON serializers
- `api/views.py` – protected API endpoints
- `templates/dashboard.html` – dashboard and charts
- `README.md` – quick-start instructions
- `docs/` – architecture, setup, API, deployment, and report documentation

## Actual implementation status

The project is functional for the required MVP scope: user accounts, homes, appliances, meter readings, CSV import, tariff calculation, dashboard, analytics, insights, and API access with ownership checks. No EEU API integration or ML forecasting was added because they were explicitly outside the approved MVP scope.
