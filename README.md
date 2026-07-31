# OFMA Website

A full website for Okeho Female Muslims' Ambassadors (OFMA) — built with Flask
(Python) and SQLite. Includes 22 public pages, working contact/volunteer/school
forms, a Paystack-ready donation flow, and an admin panel for managing blog
posts, speakers, and form submissions without touching code.

This has been tested end-to-end in development (every page, every form, the
full admin login → CRUD flow). What's left before it's fully live is plugging
in your **real Paystack keys**, **real photos**, and deploying it to a host —
all covered below.

---

## 1. Running it locally

**Requirements:** Python 3.10+

```bash
cd ofma_site
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The first run automatically creates the SQLite database (`instance/ofma.sqlite3`)
and seeds it with the real content we already have (speaker bios, summit
details) plus clearly-marked placeholders where photos/testimonials aren't
ready yet.

Visit **http://127.0.0.1:5000**

**Admin panel:** http://127.0.0.1:5000/admin/login
Default login: `admin` / `changeme123`

> ⚠️ **Change this password before going live** — see section 4.

---

## 2. Project structure

```
ofma_site/
├── app.py              # Main app: all public page routes, donation flow
├── admin.py             # Admin blueprint: login, dashboard, blog/speaker CRUD
├── db.py                 # Database connection + init helper
├── schema.sql             # SQLite table definitions
├── seed.py                 # Seeds real speaker/summit content + admin user
├── requirements.txt
├── static/
│   ├── css/style.css      # Full design system (brand colors, type, components)
│   ├── js/main.js          # Mobile nav toggle
│   └── img/                 # Put real photos here
├── templates/
│   ├── base.html            # Shared header/nav/footer
│   ├── partials/              # Reusable SVG bits (logo swirl, curve divider)
│   ├── admin/                  # Admin panel templates
│   └── *.html                   # One template per public page
└── instance/
    └── ofma.sqlite3               # Database (created on first run)
```

---

## 3. Adding real content

### Photos
Every placeholder image is a gray box that says what should go there (e.g.
"Photo — Summit 6.0"). To replace one:
1. Drop the image file into `static/img/`
2. In the relevant template, replace the `<div class="card-media">Photo</div>`
   block with `<img src="{{ url_for('static', filename='img/your-file.jpg') }}">`

### Speakers
Go to **Admin → Speakers** to edit bios, topics, and mark a speaker
"Confirmed" once finalized (the site currently shows the real Al-Istiqamah
speaker, Chairman, and Keynote roles as "To Be Confirmed" since those are
still pending your decision between the candidates we discussed).

### Blog / News
**Admin → Blog Posts → New Post**. Body field accepts basic HTML (wrap
paragraphs in `<p>` tags).

### Testimonials & Gallery
These currently seed with placeholders. There's no admin UI for these two yet
(everything else has one) — for now, edit them directly in `seed.py` and
re-run it, or add rows directly via the `testimonials` / `gallery_images`
tables. Happy to build a proper admin UI for these next if useful.

---

## 4. Before going live — a checklist

- [ ] **Change the admin password.** Either delete `instance/ofma.sqlite3` and
      re-run with a new password:
      ```bash
      export OFMA_ADMIN_PASSWORD="something-much-stronger"
      python3 -c "from db import init_db; init_db()"
      python3 seed.py
      ```
      or log in and we can add a "change password" admin page next.
- [ ] **Set a real secret key** (used to sign sessions):
      ```bash
      export OFMA_SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
      ```
- [ ] **Add your Paystack keys** (see section 5).
- [ ] **Replace placeholder photos, testimonials, and gallery images.**
- [ ] Have the **Privacy Policy** page reviewed by someone qualified — it's
      currently placeholder text, flagged as such on the page itself.

---

## 5. Connecting real donations (Paystack)

1. Create a Paystack account at paystack.com and grab your **public** and
   **secret** keys from the dashboard (use test keys first).
2. Set them as environment variables wherever you deploy:
   ```bash
   export PAYSTACK_PUBLIC_KEY="pk_live_xxxxxxxx"
   export PAYSTACK_SECRET_KEY="sk_live_xxxxxxxx"
   ```
3. That's it — `/donate` already builds the checkout flow around these keys.
   Test with a small amount using Paystack's test cards before switching to
   live keys.

The donation flow: visitor fills the form → we record a pending donation →
Paystack's inline checkout opens → on success, we verify the transaction
server-side (so a browser can't fake a successful payment) → donation is
marked `success` in the database → visible under **Admin → Donations**.

---

## 6. Deployment

This is a standard Flask app, so it deploys to any Python host. Two easy
options:

**Render.com (recommended, free tier available)**
1. Push this folder to a GitHub repo.
2. On Render: New → Web Service → connect the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app` (add `gunicorn` to `requirements.txt` first)
5. Add your environment variables (`PAYSTACK_PUBLIC_KEY`, etc.) in Render's dashboard.

**Railway.app** — similar flow, also has a generous free tier and is popular
for small Nigerian projects.

> Note: SQLite works fine at this scale, but most free hosts wipe the
> filesystem on redeploy. If that becomes an issue once you're getting regular
> donations/submissions, we should migrate to a hosted Postgres database
> (e.g. via Supabase, also free-tier friendly) — happy to do that when you're
> ready to go live for real.

---

## 7. What's built vs. what's next

**Done and tested:**
- All 22 pages, responsive, branded to match your letterhead
- Contact, volunteer, sponsor, and school-registration forms (save to database)
- Full admin panel: login, dashboard, submissions inbox, blog CRUD, speaker editor
- Donation flow wired to Paystack (needs your real keys to go fully live)

**Natural next steps, whenever you're ready:**
- Admin UI for testimonials and gallery (currently edit via `seed.py`)
- Email notifications when a form is submitted (currently only visible in admin)
- Real photos throughout
- Production deployment + Postgres migration if traffic grows
