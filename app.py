import os
from datetime import datetime, date

from flask import Flask, render_template, request, redirect, url_for, flash, abort
import requests

from db import get_db, init_db, now_iso
from admin import admin_bp

app = Flask(__name__)
app.secret_key = os.environ.get("OFMA_SECRET_KEY", "dev-secret-change-me")

# ---------------------------------------------------------------------
# Config — replace these via environment variables in production.
# ---------------------------------------------------------------------
app.config["PAYSTACK_PUBLIC_KEY"] = os.environ.get("PAYSTACK_PUBLIC_KEY", "pk_test_REPLACE_ME")
app.config["PAYSTACK_SECRET_KEY"] = os.environ.get("PAYSTACK_SECRET_KEY", "sk_test_REPLACE_ME")

SUMMIT = {
    "edition": "7.0",
    "theme": "Uncompromised: Standing Firm When the World Demands Less",
    "dates": "Saturday 19th – Sunday 20th December 2026",
    "venue": "Federal University of Agriculture and Technology (FUNATO), Okeho, Oyo State",
}

app.register_blueprint(admin_bp)


@app.context_processor
def inject_globals():
    return dict(current_year=date.today().year, summit=SUMMIT)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


def save_submission(form_type, name, email, phone, message, meta=None):
    conn = get_db()
    conn.execute(
        """INSERT INTO form_submissions (form_type, name, email, phone, message, meta, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (form_type, name, email, phone, message, meta, now_iso()),
    )
    conn.commit()
    conn.close()


# =======================================================================
# CORE PAGES
# =======================================================================

@app.route("/")
def home():
    conn = get_db()
    posts = conn.execute(
        "SELECT * FROM blog_posts ORDER BY published_at DESC LIMIT 3"
    ).fetchall()
    speakers = conn.execute(
        "SELECT * FROM speakers WHERE status='confirmed' ORDER BY sort_order LIMIT 4"
    ).fetchall()
    testimonials = conn.execute(
        "SELECT * FROM testimonials ORDER BY sort_order LIMIT 3"
    ).fetchall()
    conn.close()
    return render_template("home.html", active="home", posts=posts, speakers=speakers, testimonials=testimonials)


@app.route("/about")
def about():
    return render_template("about.html", active="about")


@app.route("/about/story")
def story():
    return render_template("story.html", active="about")


@app.route("/about/leadership")
def leadership():
    return render_template("leadership.html", active="about")


# =======================================================================
# PROGRAMS
# =======================================================================

@app.route("/programs")
def programs():
    return render_template("programs.html", active="programs")


@app.route("/programs/summit")
def summit():
    conn = get_db()
    speakers = conn.execute("SELECT * FROM speakers ORDER BY sort_order").fetchall()
    conn.close()
    return render_template("summit.html", active="programs", speakers=speakers)


@app.route("/programs/past-summits")
def past_summits():
    return render_template("past_summits.html", active="programs")


@app.route("/programs/maths-clinic")
def maths_clinic():
    return render_template("maths_clinic.html", active="programs")


# =======================================================================
# PEOPLE
# =======================================================================

@app.route("/speakers")
def speakers():
    conn = get_db()
    all_speakers = conn.execute("SELECT * FROM speakers ORDER BY sort_order").fetchall()
    conn.close()
    return render_template("speakers.html", active="people", speakers=all_speakers)


@app.route("/speakers/<slug>")
def speaker_detail(slug):
    conn = get_db()
    speaker = conn.execute("SELECT * FROM speakers WHERE slug = ?", (slug,)).fetchone()
    conn.close()
    if not speaker:
        abort(404)
    return render_template("speaker_detail.html", active="people", speaker=speaker)


@app.route("/testimonials")
def testimonials():
    conn = get_db()
    items = conn.execute("SELECT * FROM testimonials ORDER BY sort_order").fetchall()
    conn.close()
    return render_template("testimonials.html", active="people", testimonials=items)


# =======================================================================
# MEDIA
# =======================================================================

@app.route("/gallery")
def gallery():
    conn = get_db()
    images = conn.execute("SELECT * FROM gallery_images ORDER BY sort_order").fetchall()
    conn.close()
    return render_template("gallery.html", active="media", images=images)


@app.route("/videos")
def videos():
    return render_template("videos.html", active="media")


@app.route("/blog")
def blog():
    conn = get_db()
    posts = conn.execute("SELECT * FROM blog_posts ORDER BY published_at DESC").fetchall()
    conn.close()
    return render_template("blog_list.html", active="media", posts=posts)


@app.route("/blog/<slug>")
def blog_detail(slug):
    conn = get_db()
    post = conn.execute("SELECT * FROM blog_posts WHERE slug = ?", (slug,)).fetchone()
    conn.close()
    if not post:
        abort(404)
    return render_template("blog_detail.html", active="media", post=post)


# =======================================================================
# GET INVOLVED
# =======================================================================

@app.route("/donate", methods=["GET"])
def donate():
    return render_template("donate.html", active="donate")


@app.route("/donate/init", methods=["POST"])
def donate_init():
    """Record a pending donation before handing off to Paystack inline JS."""
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    amount = request.form.get("amount", "").strip()

    if not name or not email or not amount:
        flash("Please fill in your name, email, and amount.", "error")
        return redirect(url_for("donate"))

    try:
        amount_kobo = int(float(amount) * 100)
    except ValueError:
        flash("Please enter a valid amount.", "error")
        return redirect(url_for("donate"))

    reference = f"OFMA-{int(datetime.utcnow().timestamp())}"
    conn = get_db()
    conn.execute(
        "INSERT INTO donations (name, email, amount, reference, status, created_at) VALUES (?, ?, ?, ?, 'pending', ?)",
        (name, email, amount_kobo, reference, now_iso()),
    )
    conn.commit()
    conn.close()

    return render_template(
        "donate_checkout.html",
        active="donate",
        name=name,
        email=email,
        amount_kobo=amount_kobo,
        reference=reference,
        paystack_public_key=app.config["PAYSTACK_PUBLIC_KEY"],
    )


@app.route("/donate/verify")
def donate_verify():
    """Called after Paystack inline checkout completes; verifies server-side."""
    reference = request.args.get("reference")
    if not reference:
        abort(400)

    conn = get_db()
    donation = conn.execute("SELECT * FROM donations WHERE reference = ?", (reference,)).fetchone()

    status = "unverified"
    if donation:
        secret_key = app.config["PAYSTACK_SECRET_KEY"]
        try:
            resp = requests.get(
                f"https://api.paystack.co/transaction/verify/{reference}",
                headers={"Authorization": f"Bearer {secret_key}"},
                timeout=10,
            )
            data = resp.json()
            if data.get("status") and data["data"]["status"] == "success":
                status = "success"
        except requests.RequestException:
            status = "pending_manual_check"

        conn.execute("UPDATE donations SET status = ? WHERE reference = ?", (status, reference))
        conn.commit()

    conn.close()
    return render_template("donate_thanks.html", active="donate", status=status)


@app.route("/sponsor", methods=["GET", "POST"])
def sponsor():
    if request.method == "POST":
        save_submission(
            "sponsor",
            request.form.get("name"),
            request.form.get("email"),
            request.form.get("phone"),
            request.form.get("message"),
            meta=request.form.get("organisation"),
        )
        flash("Thank you — your sponsorship inquiry has been received. We'll be in touch shortly.", "success")
        return redirect(url_for("sponsor"))
    return render_template("sponsor.html", active="donate")


@app.route("/volunteer", methods=["GET", "POST"])
def volunteer():
    if request.method == "POST":
        save_submission(
            "volunteer",
            request.form.get("name"),
            request.form.get("email"),
            request.form.get("phone"),
            request.form.get("message"),
        )
        flash("Thank you for offering to volunteer — we'll reach out soon.", "success")
        return redirect(url_for("volunteer"))
    return render_template("volunteer.html", active="donate")


@app.route("/schools", methods=["GET", "POST"])
def schools():
    if request.method == "POST":
        save_submission(
            "school",
            request.form.get("name"),
            request.form.get("email"),
            request.form.get("phone"),
            request.form.get("message"),
            meta=request.form.get("school_name"),
        )
        flash("Thank you — your school's participation request has been received.", "success")
        return redirect(url_for("schools"))
    return render_template("schools.html", active="donate")


# =======================================================================
# SUPPORT
# =======================================================================

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        save_submission(
            "contact",
            request.form.get("name"),
            request.form.get("email"),
            request.form.get("phone"),
            request.form.get("message"),
        )
        flash("Thank you for reaching out — we'll respond as soon as we can.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html", active="contact")


@app.route("/faq")
def faq():
    return render_template("faq.html", active="contact")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html", active="contact")


if __name__ == "__main__":
    if not os.path.exists(os.path.join("instance", "ofma.sqlite3")):
        init_db()
        import seed
        seed.run()
    app.run(debug=True, host="0.0.0.0", port=5000)
