# Database design

The data model keeps each user’s electricity information isolated by associating homes with the authenticated user.

## Key models

- `Home`: user-owned household information
- `Appliance`: device-level assumptions, power, runtime, quantity, and active status
- `MeterReading`: actual readings with source metadata and reading date
- `Tariff`: tariff definition with effective time range
- `TariffTier`: consumption band and rate for a tariff
- `Insight`: deterministic recommendation generated per home

## Relationships

- One user can have many homes.
- One home can have many appliances.
- One home can have many meter readings.
- One tariff can have many tiers.
- One home can have many insights.

## Constraints

- Meter readings cannot be negative.
- Appliance power and runtime values cannot be negative.
- Invalid meter sequences are rejected rather than silently normalized.
- Ownership checks are enforced in the API and protected views.
