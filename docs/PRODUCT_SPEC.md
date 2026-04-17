# Aperture Estate — Product Specification

**Version:** 1.0
**Date:** 2026-04-16
**Owner:** Daniel
**Status:** Draft

---

## 1. Overview

Aperture Estate is an editorial real estate web platform for ultra-premium architectural properties. It positions listings as curated objects rather than commodities, targeting discerning buyers and advisors who expect magazine-grade presentation.

**Stack:** Django 6 · Tailwind (CDN) · PostgreSQL (SQLite fallback) · Gunicorn · Coolify/Nixpacks.

---

## 2. Goals

1. Present a curated catalog of high-end properties with editorial prose, rich galleries, and agent attribution.
2. Capture qualified buyer inquiries per-property and site-wide.
3. Give staff an admin surface to manage listings, agents, amenities, testimonials, and site copy with zero code edits.
4. Deliver a performant, SEO-friendly static-feeling experience (server-rendered Django templates + Tailwind).

## 3. Non-Goals

- Online transactions / escrow.
- Real-time chat or video tours.
- MLS / IDX integration.
- Multi-language i18n (v1 is English only).
- User accounts for buyers (inquiries are anonymous form submissions).

---

## 4. Personas

| Persona | Need |
|---|---|
| **Buyer / Advisor** | Browse curated listings, filter by location/type/price, submit inquiry to an agent. |
| **Concierge / Agent** | Receive inquiries, own a profile page, get attributed on listings. |
| **Admin / Editor** | Publish listings with images, features, amenities, and editorial copy; manage testimonials and global site settings. |

---

## 5. Information Architecture

Routes defined in [aperture/urls.py](../aperture/urls.py):

| Path | View | Purpose |
|---|---|---|
| `/` | [core.views.home](../core/views.py) | Hero, featured listings, testimonials, newsletter |
| `/about/` | [core.views.about](../core/views.py) | Story, philosophy, team (up to 4 agents) |
| `/contact/` | [core.views.contact](../core/views.py) | General inquiry form |
| `/newsletter/` (POST) | [core.views.newsletter_subscribe](../core/views.py) | Email capture |
| `/properties/` | [properties.views.listing](../properties/views.py) | Filterable paginated list |
| `/properties/<slug>/` | [properties.views.detail](../properties/views.py) | Gallery, specs, features, inquiry form |
| `/admin/` | Django admin | Staff CRUD |

---

## 6. Data Model

Source: [properties/models.py](../properties/models.py), [core/models.py](../core/models.py).

### properties app

- **Location** — `city`, `region`, `country`, `slug` (auto).
- **PropertyType** — `name`, `slug` (auto). E.g., Villa, Penthouse, Estate.
- **Amenity** — `name`, `icon` (Material Symbols).
- **Agent** — `name`, `role`, `bio`, `email`, `phone`, `photo` or `photo_url`, `featured`, `order`.
- **Property** — `title`, `slug`, `tagline`, `description`, `vision`, FK `location`, `address`, FK `property_type`, `status` ∈ {active, exclusive, new, pending, sold}, `price`, `bedrooms`, `bathrooms`, `square_feet`, `garage_spaces`, `cover_image`/`cover_image_url`, M2M `amenities`, FK `agent`, `featured`, `is_published`, timestamps.
- **PropertyImage** — FK `property`, `image`/`image_url`, `caption`, `alt`, `order`.
- **PropertyFeature** — FK `property`, `title`, `description`, `icon`, `order`.
- **Inquiry** — FK `property` (nullable), `name`, `email`, `phone`, `interest`, `message`, `created_at`, `handled`.

### core app

- **Testimonial** — `quote`, `author`, `role`, `rating` (1-5), `photo_url`, `featured`, `order`.
- **NewsletterSubscriber** — unique `email`, `created_at`.
- **SiteSettings** (singleton) — `brand_name`, `tagline`, `hq_address`, `email`, `phone`, `established_year`.

---

## 7. Features

### 7.1 Home
- Hero with up to 3 recent or featured properties.
- Featured collection (max 3).
- Testimonials (max 2 featured).
- Newsletter subscribe form.

### 7.2 Listing
- Filters: `location` (slug), `type` (slug), `price` bucket (`2-5`, `5-15`, `15-50`, `50+` in USD millions), `amenity` (id), free-text `q` (title / city / country `icontains`).
- Pagination: 9 per page.
- Published-only (`is_published=True`).

### 7.3 Detail
- Gallery (ordered `PropertyImage`).
- Specs: beds, baths, sqft, garage.
- Features (ordered cards) and amenities (chips/icons).
- Agent card with contact.
- Inquiry form → creates `Inquiry` bound to the property.
- Similar properties (same `property_type`, up to 3).

### 7.4 About
- Brand story, philosophy, featured agents (up to 4).

### 7.5 Contact
- General `InquiryForm` (no property FK).
- Success message via Django `messages`.

### 7.6 Newsletter
- `POST /newsletter/` → persists email, redirects back with flash.

### 7.7 Admin
- Full Django admin for all models above.
- `seed` management command loads canonical 7 properties + agents + amenities + testimonials + default `SiteSettings`.

---

## 8. User Flows

**Inquire on a property**
1. User opens `/properties/<slug>/`.
2. Fills inquiry form (name, email, phone, interest, message).
3. POST → `Inquiry` saved with `property` FK → redirect to detail with success flash.

**Filter listings**
1. User on `/properties/`.
2. Selects location / type / price / amenity / search text.
3. GET with querystring → filtered paginated results.

**Subscribe to newsletter**
1. User submits email on home or footer.
2. POST `/newsletter/` → dedupe by unique email → flash and redirect back.

---

## 9. Non-Functional Requirements

- **Performance:** `select_related` / `prefetch_related` on listing + detail; paginate at 9.
- **SEO:** semantic HTML, per-property slug URLs, editorial copy fields (`tagline`, `vision`).
- **Accessibility:** image `alt` on `PropertyImage`; form labels via Django forms.
- **Security:** CSRF on all forms; `is_published` gate on public queries; admin behind `/admin/` auth.
- **Resilience:** image fields support external URL fallback (`*_url`) so seeds work without uploads.
- **Observability:** Django logging defaults; inquiries flagged via `handled` boolean.

---

## 10. Deployment

Pipeline: [.github/workflows/ci-deploy.yml](../.github/workflows/ci-deploy.yml).

- **CI** on push + PR to `main`: djlint, `manage.py check`, `makemigrations --check`, tests, `collectstatic --dry-run` vs ephemeral Postgres 16.
- **CD** on green `main`: Coolify webhook (Bearer token) → Nixpacks rebuild from git.
- **Pre-deploy:** `migrate --noinput && collectstatic --noinput`.
- **Start:** `gunicorn aperture.wsgi --bind 0.0.0.0:8000`.
- **Env:** `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS`, `DB_ENGINE=postgres`, `DB_*`.

---

## 11. Success Metrics

- Inquiry conversion rate (inquiries / detail pageviews).
- Newsletter signups / week.
- Listing-to-detail CTR.
- Admin turnaround (new listing publish time).
- Page load p95 < 1.5s (server-rendered).

---

## 12. Risks & Open Questions

- **No buyer auth** — saved searches / favorites require future login layer.
- **Tailwind CDN** — fine for v1, but migrate to build pipeline if bundle control / purge needed.
- **SQLite fallback** — dev only; production must use Postgres.
- **Inquiry notifications** — currently stored only; email/Slack dispatch is TBD.
- **Image hosting** — mixed local/URL model is pragmatic now but should consolidate (S3/Cloudinary) for scale.
- **i18n** — English-only; international buyers may want ES/FR.

---

## 13. Out of Scope for v1

- Mortgage calculator, scheduling tours, map integration, saved searches, comparison view, favorites, analytics dashboard, CRM sync.
