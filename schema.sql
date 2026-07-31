DROP TABLE IF EXISTS admin_users;
DROP TABLE IF EXISTS blog_posts;
DROP TABLE IF EXISTS speakers;
DROP TABLE IF EXISTS testimonials;
DROP TABLE IF EXISTS gallery_images;
DROP TABLE IF EXISTS form_submissions;
DROP TABLE IF EXISTS donations;

CREATE TABLE admin_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE blog_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    excerpt TEXT,
    body TEXT NOT NULL,
    published_at TEXT NOT NULL,
    author TEXT DEFAULT 'OFMA Team'
);

CREATE TABLE speakers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL,
    topic TEXT,
    bio TEXT,
    day TEXT,
    status TEXT DEFAULT 'confirmed',
    sort_order INTEGER DEFAULT 0
);

CREATE TABLE testimonials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT,
    quote TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0
);

CREATE TABLE gallery_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    caption TEXT,
    category TEXT DEFAULT 'General',
    image_path TEXT,
    sort_order INTEGER DEFAULT 0
);

CREATE TABLE form_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    form_type TEXT NOT NULL,
    name TEXT,
    email TEXT,
    phone TEXT,
    message TEXT,
    meta TEXT,
    created_at TEXT NOT NULL,
    handled INTEGER DEFAULT 0
);

CREATE TABLE donations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    amount INTEGER,
    reference TEXT UNIQUE,
    status TEXT DEFAULT 'pending',
    created_at TEXT NOT NULL
);
