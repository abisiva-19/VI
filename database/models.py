import re
import unicodedata
from datetime import UTC, datetime

from werkzeug.security import check_password_hash, generate_password_hash

from database import db


def utc_now():
    """Return timezone-aware current UTC time."""
    return datetime.now(UTC)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), default="Administrator")
    role = db.Column(db.String(20), default="admin")
    created_at = db.Column(db.DateTime, default=utc_now)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(100), nullable=False)
    name_ta = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description_en = db.Column(db.Text, default="")
    description_ta = db.Column(db.Text, default="")
    icon = db.Column(db.String(50), default="newspaper")
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=utc_now)

    articles = db.relationship("Article", back_populates="category", lazy="dynamic")

    @property
    def article_count(self):
        return self.articles.filter_by(status="published").count()

    @property
    def total_article_count(self):
        return self.articles.count()

    def __repr__(self):
        return f"<Category {self.name_en}>"


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    title_ta = db.Column(db.String(255), nullable=True)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    summary = db.Column(db.Text, nullable=False)
    summary_ta = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=False)
    content_ta = db.Column(db.Text, nullable=True)

    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )
    category = db.relationship("Category", back_populates="articles")

    author = db.Column(db.String(100), default="Vithaigal Iyakkam Desk")
    author_ta = db.Column(db.String(100), default="விதை இயக்க ஆசிரியர் குழு")
    featured_image = db.Column(db.String(255), default="/static/images/placeholder.jpg")
    image_caption = db.Column(db.String(255), default="")
    video_url = db.Column(db.String(255), nullable=True)  # YouTube embed url or id
    tags = db.Column(db.String(255), default="")

    status = db.Column(
        db.String(20), default="published", index=True
    )  # 'draft', 'published', 'scheduled'
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)
    is_trending = db.Column(db.Boolean, default=False)

    published_at = db.Column(db.DateTime, default=utc_now, index=True)
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    bookmarks = db.relationship(
        "Bookmark", backref="article", cascade="all, delete-orphan", lazy="dynamic"
    )
    article_views = db.relationship(
        "ArticleView", backref="article", cascade="all, delete-orphan", lazy="dynamic"
    )

    @property
    def reading_time(self):
        word_count = len((self.content or "").split())
        minutes = max(1, round(word_count / 180))
        return minutes

    @property
    def formatted_date(self):
        if not self.published_at:
            return ""
        return self.published_at.strftime("%B %d, %Y")

    @property
    def formatted_date_ta(self):
        if not self.published_at:
            return ""
        # Tamil month mapping
        months_ta = {
            1: "ஜனவரி",
            2: "பிப்ரவரி",
            3: "மார்ச்",
            4: "ஏப்ரல்",
            5: "மே",
            6: "ஜூன்",
            7: "ஜூலை",
            8: "ஆகஸ்ட்",
            9: "செப்டம்பர்",
            10: "அக்டோபர்",
            11: "நவம்பர்",
            12: "டிசம்பர்",
        }
        day = self.published_at.day
        month = months_ta.get(self.published_at.month, "")
        year = self.published_at.year
        return f"{day} {month}, {year}"

    @staticmethod
    def extract_youtube_id(video_url):
        """Extract clean 11-char YouTube ID from any format: watch, share, shorts, embed, or bare ID."""
        if not video_url:
            return None
        url = str(video_url).strip()
        if re.match(r"^[\w-]{11}$", url):
            return url
        yt_regex = r"(?:https?:\/\/)?(?:www\.|m\.|music\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=|shorts\/))([\w-]{11})"
        match = re.search(yt_regex, url)
        return match.group(1) if match else None

    @property
    def youtube_embed_id(self):
        return Article.extract_youtube_id(self.video_url)

    @property
    def has_video(self):
        """Returns True if article has a valid video link attached."""
        return bool(
            self.youtube_embed_id or (self.video_url and str(self.video_url).strip())
        )

    @property
    def display_image(self):
        """Returns custom image or falls back to YouTube HQ thumbnail or placeholder."""
        img = (self.featured_image or "").strip()
        if img and img != "/static/images/placeholder.jpg":
            return img
        yt_id = self.youtube_embed_id
        if yt_id:
            return f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
        return "/static/images/placeholder.jpg"

    @staticmethod
    def generate_slug(text, article_id=None):
        """Generate a clean URL slug from title, with duplicate avoidance."""
        text = text.strip()
        # Transliterate or normalize Unicode
        slug = unicodedata.normalize("NFKD", text)
        slug = re.sub(r"[^\w\s-]", "", slug).strip().lower()
        slug = re.sub(r"[-\s]+", "-", slug)
        if not slug:
            slug = f"article-{int(utc_now().timestamp())}"

        # Check uniqueness
        base_slug = slug
        count = 1
        query = Article.query.filter_by(slug=slug)
        if article_id:
            query = query.filter(Article.id != article_id)
        while query.first():
            slug = f"{base_slug}-{count}"
            count += 1
            query = Article.query.filter_by(slug=slug)
            if article_id:
                query = query.filter(Article.id != article_id)
        return slug

    def __repr__(self):
        return f"<Article {self.title}>"


class BreakingNews(db.Model):
    __tablename__ = "breaking_news"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    title_ta = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=utc_now)

    @property
    def display_image(self):
        if self.image_url and self.image_url != "/static/images/logo.png":
            return self.image_url
        if self.link_url and "/article/" in self.link_url:
            slug = self.link_url.split("/article/")[-1].split("?")[0].strip("/")
            art = Article.query.filter_by(slug=slug).first()
            if art and art.featured_image:
                return art.featured_image
        return self.image_url if self.image_url else "/static/images/logo.png"

    @property
    def linked_article(self):
        if self.link_url and "/article/" in self.link_url:
            slug = self.link_url.split("/article/")[-1].split("?")[0].strip("/")
            return Article.query.filter_by(slug=slug).first()
        return None

    @property
    def formatted_date(self):
        if not self.created_at:
            return ""
        return self.created_at.strftime("%m/%d/%Y")

    @property
    def formatted_date_ta(self):
        if not self.created_at:
            return ""
        months_ta = {
            1: "ஜனவரி",
            2: "பிப்ரவரி",
            3: "மார்ச்",
            4: "ஏப்ரல்",
            5: "மே",
            6: "ஜூன்",
            7: "ஜூலை",
            8: "ஆகஸ்ட்",
            9: "செப்டம்பர்",
            10: "அக்டோபர்",
            11: "நவம்பர்",
            12: "டிசம்பர்",
        }
        return f"{self.created_at.day} {months_ta.get(self.created_at.month, '')}, {self.created_at.year}"

    def __repr__(self):
        return f"<BreakingNews {self.title}>"


class ArticleView(db.Model):
    __tablename__ = "article_views"

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(
        db.Integer, db.ForeignKey("articles.id", ondelete="CASCADE"), nullable=False
    )
    ip_address = db.Column(db.String(64), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    viewed_at = db.Column(db.DateTime, default=utc_now)


class Bookmark(db.Model):
    __tablename__ = "bookmarks"

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(
        db.Integer, db.ForeignKey("articles.id", ondelete="CASCADE"), nullable=False
    )
    session_id = db.Column(db.String(128), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=utc_now)


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=utc_now)


class NewsletterSubscriber(db.Model):
    __tablename__ = "newsletter_subscribers"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    subscribed_at = db.Column(db.DateTime, default=utc_now)


class WebsiteSetting(db.Model):
    __tablename__ = "website_settings"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    value = db.Column(db.Text, default="")
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    @classmethod
    def get_setting(cls, key, default=""):
        item = cls.query.filter_by(key=key).first()
        return item.value if item else default

    @classmethod
    def set_setting(cls, key, value):
        item = cls.query.filter_by(key=key).first()
        if not item:
            item = cls(key=key, value=value)
            db.session.add(item)
        else:
            item.value = value
        db.session.commit()
