"""
Seeds the database with real OFMA content we already have on file
(speaker bios/topics, summit details) plus clearly-marked placeholders
where real content (photos, testimonials, gallery images) isn't ready yet.

Run once after init_db(): `python seed.py`
"""
import os
from werkzeug.security import generate_password_hash
from db import get_db, now_iso

ADMIN_USERNAME = os.environ.get("OFMA_ADMIN_USER", "admin")
ADMIN_PASSWORD = os.environ.get("OFMA_ADMIN_PASSWORD", "changeme123")

SPEAKERS = [
    dict(
        name="Ustadh AbdRasheed Hashim",
        slug="ustadh-abdrasheed-hashim",
        role="Speaker — Islamic Perspective",
        topic="The Intentional Believer: Fulfilling Your Amanah Without Losing Yourself",
        bio=(
            "Ustadh AbdRasheed Hashim joins OFMA Annual Summit 7.0 to open the session "
            "\u201cThe Ideal Muslim Home\u201d from an Islamic perspective — addressing boundaries, "
            "role-intentionality, and Amanah within the family, grounded in the Sunnah."
        ),
        day="Day 2 — Sunday, 20th December 2026",
        status="confirmed",
        sort_order=1,
    ),
    dict(
        name="Sis. Nafisah Ogunbona",
        slug="sis-nafisah-ogunbona",
        role="Speaker — Psychological Perspective",
        topic="The Hidden Harm of 'Doing Too Much': Self-Neglect and Over-Parenting",
        bio=(
            "Sis. Nafisah Ogunbona brings a mental-health professional's lens to \u201cThe Ideal "
            "Muslim Home,\u201d addressing burnout, self-neglect, and the psychological cost of "
            "over-parenting."
        ),
        day="Day 2 — Sunday, 20th December 2026",
        status="confirmed",
        sort_order=2,
    ),
    dict(
        name="Mr Muheez Okunade",
        slug="muheez-okunade",
        role="Guest Speaker",
        topic="Building a Halal Brand: Turning Small Ideas into Lasting Wealth",
        bio=(
            "Mr Muheez Okunade introduces participants to Nigeria's growing halal economy and "
            "shows how ethical entrepreneurship can become a pathway to sustainable wealth "
            "creation and community development."
        ),
        day="Day 2 — Sunday, 20th December 2026",
        status="confirmed",
        sort_order=3,
    ),
    dict(
        name="Speaker To Be Confirmed",
        slug="al-istiqamah-speaker-tbc",
        role="Speaker — Al-Istiqamah Session",
        topic="Al-Istiqamah — Steadfastness on Allah's Path in Uncertain Times",
        bio=(
            "OFMA is finalising this speaker from a shortlist of respected scholars for our "
            "Day 1 session on steadfastness in faith amid modern pressures. Details will be "
            "announced here once confirmed."
        ),
        day="Day 1 — Saturday, 19th December 2026",
        status="tbc",
        sort_order=0,
    ),
    dict(
        name="Chairman of the Occasion — To Be Confirmed",
        slug="chairman-tbc",
        role="Chairman of the Occasion",
        topic=None,
        bio="OFMA is honoured to be finalising a distinguished Chairman for this year's summit.",
        day="Day 2 — Sunday, 20th December 2026",
        status="tbc",
        sort_order=4,
    ),
    dict(
        name="Keynote Speaker — To Be Confirmed",
        slug="keynote-tbc",
        role="Keynote Speaker",
        topic=None,
        bio="OFMA is finalising this year's keynote speaker. Check back soon for the announcement.",
        day="Day 2 — Sunday, 20th December 2026",
        status="tbc",
        sort_order=5,
    ),
]

TESTIMONIALS = [
    dict(
        name="Parent, OFMA Summit 6.0",
        role="Parent attendee",
        quote=(
            "[Placeholder — replace with a real quote] The parenting session changed how I talk "
            "to my teenager. I finally understood I was carrying a role that wasn't only mine to carry."
        ),
        sort_order=1,
    ),
    dict(
        name="Student, Partner School",
        role="Debate competition participant",
        quote=(
            "[Placeholder — replace with a real quote] OFMA gave me a stage to speak, and a "
            "community that believed I could stand on it."
        ),
        sort_order=2,
    ),
    dict(
        name="Community Volunteer",
        role="OFMA Summit 5.0 & 6.0",
        quote=(
            "[Placeholder — replace with a real quote] Every summit feels less like an event and "
            "more like a family reunion with a purpose."
        ),
        sort_order=3,
    ),
]

GALLERY = [
    dict(caption="Eid-al-Adha Sisters' Hangout — \"Soft Life: The Right Way\"", category="Community", image_path="/static/img/eid-adha-sisters-hangout.png", sort_order=1),
    dict(caption="OFMA Maths Clinic Magazine — 1st Edition", category="Maths Clinic", image_path="/static/img/maths-clinic-magazine-cover.jpg", sort_order=2),
    dict(caption="OFMA Annual Summit 6.0 — Opening Session", category="Summit", image_path=None, sort_order=3),
    dict(caption="Debate & Quiz Competition", category="Summit", image_path=None, sort_order=4),
    dict(caption="Community Outreach", category="Community", image_path=None, sort_order=5),
]

BLOG_POSTS = [
    dict(
        title="OFMA Annual Summit 7.0 — Save the Date",
        slug="ofma-summit-7-save-the-date",
        excerpt="This year's summit, themed \u201cUncompromised: Standing Firm When the World Demands Less,\u201d holds December 19–20, 2026 at FUNATO, Okeho.",
        body=(
            "<p>We're excited to announce that <strong>OFMA Annual Summit 7.0</strong> will hold from "
            "<strong>Saturday 19th to Sunday 20th December 2026</strong> at the <strong>Federal University "
            "of Agriculture and Technology (FUNATO), Okeho, Oyo State</strong>.</p>"
            "<p>This year's theme, <em>\u201cUncompromised: Standing Firm When the World Demands Less,\u201d</em> "
            "speaks to a challenge many of us feel quietly every day — the pressure to soften our values, "
            "dilute our faith, or shrink our ambitions just to fit in.</p>"
            "<p>Over two days, we'll bring together scholars, professionals, students, and families for "
            "sessions on faith, leadership, parenting, mental well-being, and purposeful living. More details "
            "on speakers and schedule will be published here as they're confirmed.</p>"
        ),
        published_at="2026-07-31",
        author="OFMA Team",
    ),
]


def run():
    conn = get_db()

    conn.execute(
        "INSERT OR IGNORE INTO admin_users (username, password_hash) VALUES (?, ?)",
        (ADMIN_USERNAME, generate_password_hash(ADMIN_PASSWORD)),
    )

    for s in SPEAKERS:
        conn.execute(
            """INSERT OR IGNORE INTO speakers (name, slug, role, topic, bio, day, status, sort_order)
               VALUES (:name, :slug, :role, :topic, :bio, :day, :status, :sort_order)""",
            s,
        )

    for t in TESTIMONIALS:
        conn.execute(
            """INSERT INTO testimonials (name, role, quote, sort_order)
               VALUES (:name, :role, :quote, :sort_order)""",
            t,
        )

    for g in GALLERY:
        conn.execute(
            """INSERT INTO gallery_images (caption, category, image_path, sort_order)
               VALUES (:caption, :category, :image_path, :sort_order)""",
            g,
        )

    for b in BLOG_POSTS:
        conn.execute(
            """INSERT OR IGNORE INTO blog_posts (title, slug, excerpt, body, published_at, author)
               VALUES (:title, :slug, :excerpt, :body, :published_at, :author)""",
            b,
        )

    conn.commit()
    conn.close()
    print(f"Seeded database. Admin login -> username: '{ADMIN_USERNAME}', password: '{ADMIN_PASSWORD}'")
    print("IMPORTANT: change this password immediately (see README).")


if __name__ == "__main__":
    run()
