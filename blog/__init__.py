"""
PDFEdit - Markdown Blog Engine
YAML frontmatter + Markdown icerik.
In-memory cache ile hizli erisim.
"""

import os
import time
import logging

logger = logging.getLogger(__name__)

# Lazy imports - modüller yoksa None kalır
_frontmatter = None
_markdown = None


def _ensure_imports():
    """python-frontmatter ve markdown modüllerini lazy import et."""
    global _frontmatter, _markdown
    if _frontmatter is None:
        try:
            import frontmatter as fm
            _frontmatter = fm
        except ImportError:
            logger.warning("python-frontmatter paketi bulunamadi. 'pip install python-frontmatter' calistirin.")
            return False
    if _markdown is None:
        try:
            import markdown as md
            _markdown = md
        except ImportError:
            logger.warning("markdown paketi bulunamadi. 'pip install markdown' calistirin.")
            return False
    return True


# In-memory cache
_cache = {}
_cache_ttl = 300  # 5 dakika


BLOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'posts')


def _get_posts_dir(lang):
    """Dil bazli posts dizinini dondur."""
    return os.path.join(BLOG_DIR, lang)


def _parse_post(filepath):
    """Tek bir markdown dosyasini parse et ve dict olarak dondur."""
    if not _ensure_imports():
        return None

    try:
        post = _frontmatter.load(filepath)
    except Exception as e:
        logger.error(f"Blog post parse hatasi: {filepath} - {e}")
        return None

    # Markdown -> HTML
    html_content = _markdown.markdown(
        post.content,
        extensions=['extra', 'codehilite', 'toc', 'nl2br']
    )

    # Slug: dosya adindan .md cikar
    slug = os.path.splitext(os.path.basename(filepath))[0]

    # Frontmatter alanlari
    meta = post.metadata

    # Kelime sayisi ve okuma suresi hesapla
    word_count = len(post.content.split())
    reading_time = max(1, round(word_count / 200))  # ~200 kelime/dakika

    return {
        'slug': slug,
        'title': meta.get('title', slug),
        'description': meta.get('description', ''),
        'date': str(meta.get('date', '')),
        'keywords': meta.get('keywords', ''),
        'related_tool': meta.get('related_tool', ''),
        'content': html_content,
        'raw': post.content,
        'word_count': word_count,
        'reading_time': reading_time,
    }


def get_post(slug, lang='tr'):
    """Belirli bir blog yazisini slug ve dil ile getir."""
    cache_key = f"post:{lang}:{slug}"

    # Cache kontrol
    if cache_key in _cache:
        entry = _cache[cache_key]
        if time.time() - entry['ts'] < _cache_ttl:
            return entry['data']

    posts_dir = _get_posts_dir(lang)
    filepath = os.path.join(posts_dir, f"{slug}.md")

    if not os.path.isfile(filepath):
        return None

    post = _parse_post(filepath)
    if post:
        _cache[cache_key] = {'data': post, 'ts': time.time()}
    return post


def get_all_posts(lang='tr'):
    """Tum blog yazilarini listele (tarihe gore ters sirali)."""
    cache_key = f"all:{lang}"

    # Cache kontrol
    if cache_key in _cache:
        entry = _cache[cache_key]
        if time.time() - entry['ts'] < _cache_ttl:
            return entry['data']

    posts_dir = _get_posts_dir(lang)
    if not os.path.isdir(posts_dir):
        return []

    posts = []
    for filename in os.listdir(posts_dir):
        if not filename.endswith('.md'):
            continue
        filepath = os.path.join(posts_dir, filename)
        post = _parse_post(filepath)
        if post:
            posts.append(post)

    # Tarihe gore ters sirala (en yeni en ustte)
    posts.sort(key=lambda p: p.get('date', ''), reverse=True)

    _cache[cache_key] = {'data': posts, 'ts': time.time()}
    return posts


def clear_cache():
    """Tum cache'i temizle."""
    global _cache
    _cache = {}
