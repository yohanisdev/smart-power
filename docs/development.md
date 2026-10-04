# Development guidance

## Conventions

- Keep business logic in service modules instead of view functions.
- Keep API permissions and user ownership checks explicit.
- Validate meter values before saving.
- Keep actual consumption and estimated consumption separate in code and UI wording.
- Prefer deterministic rules over dynamic AI features in the MVP.

## Testing

Use:

```bash
python manage.py test
```

## Versioning

This project is intentionally modular so a future React frontend or ML layer can be added without redesigning the app structure.
