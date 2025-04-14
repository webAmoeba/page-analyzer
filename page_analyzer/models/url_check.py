import requests
from page_analyzer.models.url import get_connection


def create(url_id, url_name):
    try:
        response = requests.get(url_name)
        response.raise_for_status()
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO url_checks (url_id, status_code) "
            "VALUES (%s, %s) RETURNING id, status_code, created_at",
            (url_id, response.status_code)
        )
        check_data = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            'id': check_data[0],
            'status_code': check_data[1],
            'created_at': check_data[2]
        }
    except requests.RequestException:
        return None


def get_checks_for_url(url_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, status_code, created_at FROM url_checks "
        "WHERE url_id = %s ORDER BY id DESC",
        (url_id,)
    )
    checks = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{
        'id': check[0],
        'status_code': check[1],
        'created_at': check[2]
    } for check in checks]
