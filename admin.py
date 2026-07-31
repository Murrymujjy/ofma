import re
from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash

from db import get_db, now_iso

admin_bp = Blueprint("admin", __name__, url_prefix="/admin", template_folder="templates/admin")


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_id"):
            return redirect(url_for("admin.login"))
        return view(*args, **kwargs)
    return wrapped


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        conn = get_db()
        user = conn.execute("SELECT * FROM admin_users WHERE username = ?", (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user["password_hash"], password):
            session["admin_id"] = user["id"]
            session["admin_username"] = user["username"]
            return redirect(url_for("admin.dashboard"))
        flash("Invalid username or password.", "error")
    return render_template("admin/login.html")


@admin_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@login_required
def dashboard():
    conn = get_db()
    counts = {
        "submissions": conn.execute("SELECT COUNT(*) c FROM form_submissions").fetchone()["c"],
        "unhandled": conn.execute("SELECT COUNT(*) c FROM form_submissions WHERE handled = 0").fetchone()["c"],
        "donations": conn.execute("SELECT COUNT(*) c FROM donations WHERE status='success'").fetchone()["c"],
        "posts": conn.execute("SELECT COUNT(*) c FROM blog_posts").fetchone()["c"],
    }
    recent = conn.execute(
        "SELECT * FROM form_submissions ORDER BY created_at DESC LIMIT 6"
    ).fetchall()
    conn.close()
    return render_template("admin/dashboard.html", counts=counts, recent=recent)


@admin_bp.route("/submissions")
@login_required
def submissions():
    conn = get_db()
    items = conn.execute("SELECT * FROM form_submissions ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("admin/submissions.html", items=items)


@admin_bp.route("/submissions/<int:sub_id>/handled")
@login_required
def mark_handled(sub_id):
    conn = get_db()
    conn.execute("UPDATE form_submissions SET handled = 1 WHERE id = ?", (sub_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin.submissions"))


@admin_bp.route("/blog")
@login_required
def blog_list():
    conn = get_db()
    posts = conn.execute("SELECT * FROM blog_posts ORDER BY published_at DESC").fetchall()
    conn.close()
    return render_template("admin/blog_list.html", posts=posts)


@admin_bp.route("/blog/new", methods=["GET", "POST"])
@login_required
def blog_new():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        slug = slugify(title)
        conn = get_db()
        conn.execute(
            """INSERT INTO blog_posts (title, slug, excerpt, body, published_at, author)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                title, slug,
                request.form.get("excerpt"),
                request.form.get("body"),
                request.form.get("published_at") or now_iso()[:10],
                request.form.get("author") or "OFMA Team",
            ),
        )
        conn.commit()
        conn.close()
        flash("Post published.", "success")
        return redirect(url_for("admin.blog_list"))
    return render_template("admin/blog_form.html", post=None)


@admin_bp.route("/blog/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def blog_edit(post_id):
    conn = get_db()
    post = conn.execute("SELECT * FROM blog_posts WHERE id = ?", (post_id,)).fetchone()
    if request.method == "POST":
        conn.execute(
            """UPDATE blog_posts SET title=?, excerpt=?, body=?, published_at=?, author=?
               WHERE id=?""",
            (
                request.form.get("title"),
                request.form.get("excerpt"),
                request.form.get("body"),
                request.form.get("published_at"),
                request.form.get("author"),
                post_id,
            ),
        )
        conn.commit()
        conn.close()
        flash("Post updated.", "success")
        return redirect(url_for("admin.blog_list"))
    conn.close()
    return render_template("admin/blog_form.html", post=post)


@admin_bp.route("/blog/<int:post_id>/delete")
@login_required
def blog_delete(post_id):
    conn = get_db()
    conn.execute("DELETE FROM blog_posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    flash("Post deleted.", "success")
    return redirect(url_for("admin.blog_list"))


@admin_bp.route("/speakers")
@login_required
def speakers_admin():
    conn = get_db()
    items = conn.execute("SELECT * FROM speakers ORDER BY sort_order").fetchall()
    conn.close()
    return render_template("admin/speakers.html", speakers=items)


@admin_bp.route("/speakers/<int:speaker_id>/edit", methods=["GET", "POST"])
@login_required
def speaker_edit(speaker_id):
    conn = get_db()
    sp = conn.execute("SELECT * FROM speakers WHERE id = ?", (speaker_id,)).fetchone()
    if request.method == "POST":
        conn.execute(
            """UPDATE speakers SET name=?, role=?, topic=?, bio=?, day=?, status=? WHERE id=?""",
            (
                request.form.get("name"),
                request.form.get("role"),
                request.form.get("topic"),
                request.form.get("bio"),
                request.form.get("day"),
                request.form.get("status"),
                speaker_id,
            ),
        )
        conn.commit()
        conn.close()
        flash("Speaker updated.", "success")
        return redirect(url_for("admin.speakers_admin"))
    conn.close()
    return render_template("admin/speaker_form.html", speaker=sp)


@admin_bp.route("/donations")
@login_required
def donations_admin():
    conn = get_db()
    items = conn.execute("SELECT * FROM donations ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("admin/donations.html", items=items)
