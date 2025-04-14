import os
import psycopg2
import validators
from urllib.parse import urlparse


def get_connection():
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise ValueError('DATABASE_URL is not set')
    return psycopg2.connect(DATABASE_URL)


def normalize_url(url):
    parsed = urlparse(url)
    scheme = parsed.scheme or 'http'
    netloc = parsed.netloc
    
    if not netloc and parsed.path:
        netloc = parsed.path.split('/')[0]
        if netloc:
            path_parts = parsed.path.split('/')
            if len(path_parts) > 1:
                path = '/'.join(path_parts[1:])
            else:
                path = ''
            parsed = parsed._replace(netloc=netloc, path=path)
    
    return f"{scheme}://{netloc.lower()}"


def validate(url):
    errors = []
    if len(url) > 255:
        errors.append('URL превышает 255 символов')
    if not validators.url(url):
        errors.append('Некорректный URL')
    return errors


def get_all():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM urls ORDER BY id DESC")
    urls = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(id=url[0], name=url[1]) for url in urls]


def get_by_id(url_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, created_at FROM urls WHERE id = %s",
        (url_id,)
    )
    url_data = cursor.fetchone()
    cursor.close()
    conn.close()
    if url_data is None:
        return None
    return dict(id=url_data[0], name=url_data[1], created_at=url_data[2])


def exists(url):
    normalized_url = normalize_url(url)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM urls WHERE name = %s", (normalized_url,))
    exists = cursor.fetchone()
    cursor.close()
    conn.close()
    return exists is not None


def create(url):
    normalized_url = normalize_url(url)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO urls (name) VALUES (%s) RETURNING id",
        (normalized_url,)
    )
    url_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return url_id
