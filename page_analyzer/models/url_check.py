import requests
from bs4 import BeautifulSoup
from page_analyzer.models.url import get_connection


def create(url_id, url_name):
    try:
        response = requests.get(url_name)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        h1_tag = soup.find('h1')
        h1_text = h1_tag.text.strip() if h1_tag else ''
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO url_checks (url_id, status_code, h1) "
            "VALUES (%s, %s, %s) RETURNING id, status_code, h1, created_at",
            (url_id, response.status_code, h1_text)
        )
        check_data = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            'id': check_data[0],
            'status_code': check_data[1],
            'h1': check_data[2],
            'created_at': check_data[3]
        }
    except requests.RequestException:
        return None


def get_checks_for_url(url_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, status_code, h1, created_at FROM url_checks "
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
        'created_at': check[3]
    } for check in checks]
