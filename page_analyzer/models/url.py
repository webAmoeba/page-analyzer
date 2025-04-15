import os
from urllib.parse import urlparse

import psycopg2
import validators


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


def get_all_with_latest_check():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            urls.id, 
            urls.name, 
            url_checks.created_at, 
            url_checks.status_code 
        FROM urls 
        LEFT JOIN (
            SELECT DISTINCT ON (url_id) 
                url_id, 
                created_at, 
                status_code 
            FROM url_checks 
            ORDER BY url_id, created_at DESC
        ) AS url_checks ON urls.id = url_checks.url_id 
        ORDER BY urls.id DESC
    """)
    urls = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(
        id=url[0], 
        name=url[1], 
        last_check_at=url[2], 
        status_code=url[3]
    ) for url in urls]


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


def get_id_by_name(url_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM urls WHERE name = %s", (url_name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result[0]
    return None


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
