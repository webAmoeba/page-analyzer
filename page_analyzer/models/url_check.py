from page_analyzer.models.url import get_connection


def create(url_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO url_checks (url_id) VALUES (%s) RETURNING id, created_at",
        (url_id,)
    )
    check_data = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return {
        'id': check_data[0],
        'created_at': check_data[1]
    }


def get_checks_for_url(url_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, created_at FROM url_checks "
        "WHERE url_id = %s ORDER BY id DESC",
        (url_id,)
    )
    checks = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{'id': check[0], 'created_at': check[1]} for check in checks]
