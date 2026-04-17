# Aperture Estate

Editorial real estate site built from the `stitch_wireframe_inmobiliario_elegante/` wireframes.

**Stack:** Django 6 · Tailwind (CDN) · PostgreSQL (SQLite fallback).

## Quick start

```bash
uv sync
cp .env.example .env          # edit DB creds if using Postgres
uv run python manage.py migrate
uv run python manage.py seed
uv run python manage.py runserver
```

Admin: `/admin/` (user `admin`, pass `admin` if you ran `createsuperuser` with those values).

## Environment

Set `DB_ENGINE=postgres` (default) or `DB_ENGINE=sqlite` in `.env`.

Postgres example:
```bash
createdb aperture
createuser aperture --pwprompt
```

## Structure

- `aperture/` — project settings and URLs
- `core/` — home, about, contact, newsletter, testimonials, `SiteSettings`
- `properties/` — `Property`, `Location`, `PropertyType`, `Amenity`, `Agent`, `PropertyImage`, `PropertyFeature`, `Inquiry`
- `templates/` — `base.html`, shared `partials/`, page templates
- `static/css/site.css` — small supplemental styles on top of Tailwind CDN
- `stitch_wireframe_inmobiliario_elegante/` — source wireframes (reference only)

## Seed

`uv run python manage.py seed` loads the seven wireframe properties (Alabaster Pavilion, Shadow & Timber Lodge, Horizon Point Estate, Villa di Smeraldo, Zenith Penthouse, Obsidian Sanctuary, Aurelian Estate) plus agents, amenities, testimonials, and default `SiteSettings`.

## Pages

- `/` — home (hero search, bento collection, testimonials, newsletter)
- `/properties/` — filterable listing with pagination
- `/properties/<slug>/` — detail page with gallery, specs, features, agent inquiry form
- `/about/` — story, philosophy, team
- `/contact/` — inquiry form
