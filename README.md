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

## Deployment

CI + deploy pipeline en [.github/workflows/ci-deploy.yml](.github/workflows/ci-deploy.yml).

- **CI** (push + PR a `main`): djlint, `manage.py check`, `makemigrations --check`, tests, `collectstatic --dry-run` contra Postgres 16 efímero.
- **Deploy** (solo push a `main` tras CI verde): llama al webhook de Coolify con token Bearer. Coolify rebuild con Nixpacks desde git.

### Secrets GitHub

Settings → Secrets and variables → Actions → New repository secret:

| Secret | Fuente en Coolify |
|---|---|
| `COOLIFY_WEBHOOK_URL` | App → **Webhooks** → URL completa de deploy (incluye `?uuid=...`) |
| `COOLIFY_API_TOKEN` | Perfil → **Keys & Tokens** → API tokens → crear con scope `deploy` |

### Config requerida en Coolify

Nixpacks **no** corre `migrate` ni `collectstatic` solo. Ajustar en la app de Coolify:

- **Environment variables**: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS=<dominio>`, `DB_ENGINE=postgres`, `DB_*` apuntando al Postgres del stack.
- **Pre-deploy command**:
  ```bash
  python manage.py migrate --noinput && python manage.py collectstatic --noinput
  ```
- **Start command**:
  ```bash
  gunicorn aperture.wsgi --bind 0.0.0.0:8000
  ```
- Vincular base Postgres como servicio dentro del proyecto Coolify.

### Trigger manual

Actions tab → **CI + Deploy** → Run workflow (usa `workflow_dispatch`).
