from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import psycopg2
from page_analyzer.db import get_url_data

app = Flask(__name__)
load_dotenv()

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form["url"]
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM urls WHERE name = %s", (url,))
            exists = cursor.fetchone()
            if exists:
                return render_template(
                    'index.html',
                    message='Страница уже существует'
                )
            cursor.execute("INSERT INTO urls (name) VALUES (%s)", (url,))
            conn.commit()
        return render_template(
            'index.html',
            message='Страница успешно добавлена'
        )
    return render_template('index.html')


@app.route("/urls")
def urls():
    return render_template('urls.html')


@app.route('/urls/<id>')
def get_one_url(id):
    url_data = get_url_data(id)
    if not url_data:
        return render_template('one_url.html', error='URL не найден')
    return render_template('one_url.html', url=url_data)


@app.errorhandler(404)
def not_found(error):
    return 'Oops!', 404


@app.template_filter('dateformat')
def dateformat(date):
    return date.strftime("%Y-%m-%d")


if __name__ == "__main__":
    app.run(debug=True)
