import requests
from bs4 import BeautifulSoup

from page_analyzer.models.url import get_connection


def create(url_id, url_name):
    try:
        response = requests.get(url_name)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Ошибка при запросе к {url_name}: {e}")

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        h1_tag = soup.find('h1')
        h1_text = h1_tag.text.strip() if h1_tag else ''
        title_tag = soup.find('title')
        title_text = title_tag.text.strip() if title_tag else ''
        description_tag = soup.find('meta', attrs={'name': 'description'})
        description_text = description_tag['content'].strip() \
            if description_tag else ''
    except Exception as e:
        raise RuntimeError(f"Ошибка при парсинге HTML: {e}")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO url_checks (url_id, status_code, h1, title,
            description) """
            "VALUES (%s, %s, %s, %s, %s) "
            "RETURNING id, status_code, h1, title, description, created_at",
            (
                url_id,
                response.status_code,
                h1_text,
                title_text,
                description_text
            )
        )
        check_data = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        raise RuntimeError(f"Ошибка при работе с базой данных: {e}")

    return {
        'id': check_data[0],
        'status_code': check_data[1],
        'h1': check_data[2],
        'title': check_data[3],
        'description': check_data[4],
        'created_at': check_data[5]
    }


def get_checks_for_url(url_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, status_code, h1, title, description, created_at FROM \
            url_checks "
        "WHERE url_id = %s ORDER BY id DESC",
        (url_id,)
    )
    checks = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{
        'id': check[0],
        'status_code': check[1],
        'h1': check[2],
        'title': check[3],
        'description': check[4],
        'created_at': check[5]
    } for check in checks]
