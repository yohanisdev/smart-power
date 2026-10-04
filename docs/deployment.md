# Deployment notes

This project is ready for a standard Django deployment pattern but is not configured as a production deployment by default.

## Production assumptions

- `DEBUG=False`
- strong `SECRET_KEY`
- secure environment-driven database settings
- HTTPS termination at the reverse proxy or load balancer
- static files served via a real web server or WhiteNoise in a production-ready environment
- PostgreSQL credentials stored outside the repository

## Suggested stack

- Nginx or a reverse proxy
- Gunicorn or uWSGI
- PostgreSQL database
- environment variables managed by the deployment platform

## Important note

This is a development-ready MVP, not a production hardening pass for all attack surfaces.
