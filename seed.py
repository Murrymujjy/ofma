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
        name="OFMA Programme Participant",
        role="Debate Competitor, 2020 &middot; Now at Obafemi Awolowo University",
        quote=(
            "I remember vividly that I was one of the representatives of the debate competition "
            "organized by OFMA in 2020. Alhamdulillahi, we came second. Sister Mujeebah asked each "
            "of us the university we were aspiring to get admitted to, and I boldly responded "
            "\u2018Obafemi Awolowo University\u2019 because that\u2019s my dream school. Alhamdulillahi, "
            "I am now a bona fide student of Obafemi Awolowo University."
        ),
        sort_order=1,
    ),
    dict(
        name="OFMA Programme Participant",
        role="Long-time attendee",
        quote=(
            "I have gained a deeper understanding of the Deen \u2014 how to become a better woman "
            "before marriage, a better daughter, a caring sister, and above all, a devoted servant "
            "of my Rabb. I pray that Allah accepts this as an act of \u1e63adaqah jaariyah and continues "
            "to make it a means of guidance for countless sisters."
        ),
        sort_order=2,
    ),
    dict(
        name="OFMA Programme Participant",
        role="Attendee since secondary school",
        quote=(
            "It's a program that, back then when we were in secondary school, we would be excited "
            "about whenever OFMA was near. I don't usually forget the lecturers, topics, or even the "
            "little things around the program \u2014 I have benefited from it in so many ways."
        ),
        sort_order=3,
    ),
    dict(
        name="OFMA Programme Participant",
        role="Attendee",
        quote=(
            "OFMA has shaped me in ways I couldn't have imagined. Every session left me with valuable "
            "lessons to reflect on. It has taught me to face challenges with courage, resilience, and "
            "faith rather than fear \u2014 and to never give up, no matter what."
        ),
        sort_order=4,
    ),
    dict(
        name="OFMA Programme Participant",
        role="Attendee",
        quote=(
            "OFMA has given me gifts of people \u2014 strangers turned friends and big sisters \u2014 "
            "alongside immense knowledge and skills. May Allah bless the organisers and donors and "
            "accept it as an act of Ibadah."
        ),
        sort_order=5,
    ),
    dict(
        name="OFMA Programme Participant",
        role="Attendee",
        quote=(
            "Listening to different sisters and speakers made me realise there is so much to learn, "
            "especially as a young Muslimah growing in this generation. It has shaped the way I think "
            "and made me more conscious and intentional in my choices."
        ),
        sort_order=6,
    ),
]

GALLERY = [
    dict(caption="Eid-al-Adha Sisters' Hangout 2026 — Group Photo", category="Community", image_path="/static/img/gallery/eid-hangout-2026-group.jpg", sort_order=1),
    dict(caption="OFMA Summit 6.0 — Certificate of Participation Presentation", category="Summit", image_path="/static/img/gallery/summit6-certificate-1.jpg", sort_order=2),
    dict(caption="OFMA Summit 6.0 — Debate & Quiz Winners", category="Summit", image_path="/static/img/gallery/summit6-certificate-2.jpg", sort_order=3),
    dict(caption="OFMA Summit 6.0 — Group Photo, Okeho Central Mosque", category="Summit", image_path="/static/img/gallery/summit6-group-mosque.jpg", sort_order=4),
    dict(caption="OFMA Magazine Launch — Al-Qawareer, Maiden Edition", category="Publications", image_path="/static/img/gallery/summit6-magazine-launch.jpg", sort_order=5),
    dict(caption="OFMA Maths Clinic — Students & Volunteers", category="Maths Clinic", image_path="/static/img/gallery/mathsclinic-group-1.jpg", sort_order=6),
    dict(caption="OFMA Maths Clinic — Guests & Dignitaries", category="Maths Clinic", image_path="/static/img/gallery/mathsclinic-dignitaries.jpg", sort_order=7),
    dict(caption="OFMA Maths Clinic — Closing Group Photo", category="Maths Clinic", image_path="/static/img/gallery/mathsclinic-group-2.jpg", sort_order=8),
    dict(caption="OFMA Magazine — Maiden Edition Cover", category="Publications", image_path="/static/img/ofma-magazine-cover.png", sort_order=9),
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
