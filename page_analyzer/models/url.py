import os
import psycopg2
import validators


def get_connection():
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise ValueError('DATABASE_URL is not set')
    return psycopg2.connect(DATABASE_URL)


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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM urls WHERE name = %s", (url,))
    exists = cursor.fetchone()
    cursor.close()
    conn.close()
    return exists is not None


def create(url):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO urls (name) VALUES (%s) RETURNING id",
        (url,)
    )
    url_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return url_id
