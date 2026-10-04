# API overview

The project includes a REST API under `/api/` with session-based authentication.

## Authentication

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `GET /api/auth/me/`

## Resource APIs

- `GET /api/homes/`
- `POST /api/homes/`
- `GET /api/homes/<id>/`
- `PUT /api/homes/<id>/`
- `DELETE /api/homes/<id>/`

- `GET /api/appliances/`
- `POST /api/appliances/`
- `GET /api/appliances/<id>/`
- `PUT /api/appliances/<id>/`
- `DELETE /api/appliances/<id>/`

- `GET /api/readings/`
- `POST /api/readings/`
- `GET /api/readings/<id>/`
- `PUT /api/readings/<id>/`
- `DELETE /api/readings/<id>/`

- `GET /api/analytics/daily/`
- `GET /api/analytics/weekly/`
- `GET /api/analytics/monthly/`
- `GET /api/analytics/actual-vs-estimated/`
- `GET /api/dashboard/`

## Ownership rule

Every queryset is filtered by `home__user=request.user` or the equivalent relationship so a user cannot read another user’s household data.
