# விதை இயக்கம் | Vithaigal Iyakkam
### Professional Tamil Digital News & Content Publishing Platform

A modern, full-featured digital newspaper and content publishing platform built strictly with **HTML5, CSS3, Vanilla JavaScript, Python Flask, and SQLite**.

---

## 🌟 Key Highlights & Design Philosophy

- **Zero Heavy Frontend Frameworks**: Completely free of React, Next.js, Vue, Node.js, PHP, or Django. Everything is powered by native **Vanilla JavaScript** and **Jinja2**.
- **Editorial Design System**: Deep Navy (`#0B192C`), Warm Editorial White (`#FAFAF9`), and High-Contrast Coral-Orange (`#FF5722`) accents.
- **Dual-Language Architecture (தமிழ் & English)**: Seamless top-bar toggle allowing visitors to switch between authentic Tamil and English across navigation, dates, headings, and metadata.
- **Dark & Light Mode**: Instant, persistent theme switching with automatic system detection and `localStorage` caching.
- **Dynamic Content Engine**: 100% of articles, categories, breaking tickers, statistics, views, and bookmarks are backed by **SQLite** through **Flask-SQLAlchemy**.
- **SEO-Friendly URLs**: Automatic generation of clean, transliterated unique URL slugs (e.g. `/article/keezhadi-phase-10-sangam-era-artifacts-discovered`).

---

## 🚀 Public Platform Features

1. **Editorial Homepage (`/`)**:
   - **Header & Navigation**: Bilingual logo, live clock, today's date, breaking news counter, search bar with autocomplete suggestions, mobile drawer.
   - **Breaking News Ticker**: Dynamic animated marquee pulled from the `breaking_news` table with pause-on-hover and next/prev controls.
   - **Lead & Sub-Featured News Grid**: Hero banner spotlighting top investigative stories with reading time and view count.
   - **Latest News Stream**: Real-time article feed with category badges, author attribution, and publication dates.
   - **Curated Category Sections**: Dedicated showcases for Tamil Nadu, History, India, Cinema, Jobs, and World.
   - **Trending & Most-Read Rankings**: Ranked 1 to 5 based on actual SQLite reader view counts.
   - **Featured Video Hub**: 16:9 responsive YouTube player embeds and documentary previews.
   - **Interactive Newsletter Signup**: AJAX subscription with instant toast notifications.

2. **Category Pages (`/category/<slug>`)**:
   - Covers all 7 core desks:
     - **History (வரலாறு)**: `history`
     - **Tamil Nadu (தமிழ்நாடு)**: `tamil-nadu`
     - **India (இந்தியா)**: `india`
     - **World (உலகம்)**: `world`
     - **Cinema (சினிமா)**: `cinema`
     - **Jobs (தொழில் & வேலைவாய்ப்பு)**: `jobs`
     - **YouTube (யூடியூப் & வீடியோ)**: `youtube`
   - In-category search, sorting filters (Latest, Most Viewed, Oldest), and pagination.

3. **Individual Article Page (`/article/<slug>`)**:
   - High-resolution featured image with captions.
   - Automatic real-time view tracking (`views += 1`) and client IP/agent logging.
   - Reading time estimation (calculated from word count).
   - Rich typography with lead paragraphs, blockquotes, subheadings, and lists.
   - Embedded YouTube video player for multimedia journalism.
   - Direct social sharing: **WhatsApp** (one-click prefilled message), Twitter/X, Facebook, Telegram, and Copy Link.
   - Interactive bookmark button with live counter updates.
   - Related articles from the same news desk.

4. **Search Page (`/search`)**:
   - Real-time search across titles, summaries, contents, authors, and tags in both Tamil and English.
   - Category filtering dropdown and sorting controls.
   - Instant live dropdown suggestions in navbar.

5. **Bookmarks Hub (`/bookmarks`)**:
   - Session-based bookmarking allowing readers to save stories for later reading.

6. **Contact Desk (`/contact`)**:
   - Direct message dispatch storing inquiries into SQLite `contact_messages`.
   - Editorial headquarters address, phone, and social channel links.

---

## 🛠️ Secure Admin Dashboard (`/admin`)

- **Secure Authentication & Registration**: Protected sessions, Werkzeug password hashing (PBKDF2/SHA-256), custom administrator self-registration at `/admin/register`, and automatic redirects for unauthorized access.
- **Dashboard Overview (`/admin/dashboard`)**:
  - Real SQLite statistics: Total Articles, Published, Drafts, Scheduled, Views, Categories, Messages, and Subscribers.
  - Interactive HTML5 Canvas charts: Category Distribution and Publication Status (pure Vanilla JS, zero third-party chart dependencies).
- **Article Management (CRUD)**:
  - Add, edit, delete, publish, draft, and schedule articles.
  - Drag-and-drop featured image upload with live client-side preview before saving.
  - File format validation (JPG, PNG, WEBP, GIF) and file size checks.
  - Automatic SEO slug generator.
- **Category Management**:
  - Create, update, and safely delete categories. Prevents orphaned article destruction by safely unlinking associated articles.
- **Breaking News Management**:
  - Add, edit, delete, and toggle ticker headline visibility with instant effect on the public homepage.
- **Reader Feedback & Subscribers**:
  - Manage contact form submissions (mark read/unread, reply by email).
  - Manage newsletter subscriber list.
- **Settings & Security**:
  - Customize portal title, tagline, newsroom contacts, and social media handles.
  - Change admin password with validation.

---

## 📂 Project Architecture

```
VI/
├── app.py                      # Flask Application Factory & Server Entrypoint
├── config.py                   # Configuration (DB URI, upload folder, max sizes)
├── requirements.txt            # Python Dependencies
├── test_platform.py            # Automated Unit & Integration Test Suite
├── README.md                   # Complete Documentation
├── database/
│   ├── __init__.py             # SQLAlchemy instance initialization
│   ├── models.py               # Models: User, Article, Category, BreakingNews, etc.
│   └── seed_data.py            # Comprehensive bilingual Tamil/English news seeder
├── routes/
│   ├── __init__.py
│   ├── public.py               # Public portal routes, search, bookmarks, APIs
│   ├── admin.py                # Admin dashboard & full CRUD routes
│   └── auth.py                 # Admin login, logout, and session guard
├── templates/
│   ├── base.html               # Master layout with bilingual navbar & footer
│   ├── index.html              # Homepage with hero, latest, categories, videos
│   ├── category.html           # Category archives with search & pagination
│   ├── article.html            # Article detail page with sharing & view count
│   ├── search.html             # Multi-field search results
│   ├── bookmarks.html          # Saved reading list
│   ├── contact.html            # Contact form & office details
│   └── admin/
│       ├── base_admin.html     # Admin layout with sidebar & topbar
│       ├── login.html          # Admin authentication page
│       ├── dashboard.html      # Metrics cards & HTML5 Canvas charts
│       ├── articles.html       # Article listing & quick status toggles
│       ├── add_article.html    # Add article form with live image preview
│       ├── edit_article.html   # Edit article form
│       ├── categories.html     # Category CRUD & safe deletion
│       ├── breaking_news.html  # Ticker headline manager
│       ├── messages.html       # Contact message inbox
│       ├── subscribers.html    # Newsletter subscriber list
│       └── settings.html       # Website settings & password updater
├── static/
│   ├── css/
│   │   ├── style.css           # Public responsive stylesheet & dark mode
│   │   └── admin.css           # Corporate admin dashboard stylesheet
│   ├── js/
│   │   ├── main.js             # Vanilla JS: Ticker, live search, bookmarks, theme
│   │   └── admin.js            # Vanilla JS: Dropzone, slug generator, canvas charts
│   └── images/
│       ├── logo.svg            # Custom Vithaigal Iyakkam branding emblem
│       ├── placeholder.jpg     # High-res fallback news graphic
│       └── uploads/            # Server-side user uploaded images
└── instance/
    └── vithaigal.db            # SQLite database (auto-created on startup)
```

---

## 💻 Step-by-Step Installation & Run Guide (Windows / Linux / macOS)

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.
Verify in PowerShell or Terminal:
```powershell
python --version
```

### 2. Navigate to Project Directory
```powershell
cd S:\VI
```

### 3. Create & Activate a Virtual Environment (Optional but Recommended)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies
```powershell
pip install -r requirements.txt
```
*(Packages: Flask, Flask-SQLAlchemy, Werkzeug, Pillow)*

### 5. Run the Application
```powershell
python app.py
```

On initial startup, the platform will automatically:
1. Initialize the SQLite database at `instance/vithaigal.db`.
2. Seed all 7 categories with Tamil and English descriptions.
3. Populate authentic, verified articles across Keezhadi history, Tamil Nadu industry, ISRO space missions, Kollywood cinema, TNPSC job alerts, and YouTube documentaries.
4. Launch the local web server on **`http://127.0.0.1:5000`**.

### 6. Accessing the Platform
- **Public Portal**: Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.
- **Admin Dashboard**: Open [http://127.0.0.1:5000/admin/register](http://127.0.0.1:5000/admin/register) to register your administrator account, or [http://127.0.0.1:5000/admin/login](http://127.0.0.1:5000/admin/login) to sign in.

---

## 🧪 Running the Automated Test Suite

To verify all 10 modules, routes, authentication, CRUD operations, view increments, and search capabilities:
```powershell
python test_platform.py
```
Expected output:
```
Ran 10 tests in ~11s
OK
[PASS] test_01_public_homepage
[PASS] test_02_category_page
[PASS] test_03_article_page_and_view_count
[PASS] test_04_live_search_and_search_page
[PASS] test_05_bookmark_toggle_and_bookmarks_page
[PASS] test_06_contact_and_newsletter
[PASS] test_07_language_toggle
[PASS] test_08_admin_protection_and_login
[PASS] test_09_admin_article_crud
[PASS] test_10_admin_category_and_breaking_news
```

---

## 🔒 Security Best Practices Implemented

- **Password Hashing**: Passwords are never stored in plain text; hashed using `werkzeug.security.generate_password_hash`.
- **Admin Route Guarding**: Custom `@login_required` decorator validates session state on every `/admin/*` endpoint.
- **File Upload Sanitization**: Validates extensions (`jpg`, `png`, `webp`, `gif`), enforces a 16MB server limit and 5MB client check, and saves with unique hex filenames to prevent overwrites or path traversal attacks.
- **Safe Category Deletion**: Prevents accidental cascading loss of published articles when managing categories.
- **SQL Injection Prevention**: All database queries utilize SQLAlchemy ORM parameterized queries.

