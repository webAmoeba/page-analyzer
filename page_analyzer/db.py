import os
import psycopg2


def connection(db_url):
    return psycopg2.connect(db_url)


def get_db():
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise ValueError('DATABASE_URL is not set')
    return connection(db_url)


def get_url_data(url_id):
    conn = get_db()
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


def get_all_urls():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM urls ORDER BY id DESC")
    urls = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(id=url[0], name=url[1]) for url in urls]
