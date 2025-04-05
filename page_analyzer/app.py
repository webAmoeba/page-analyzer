from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import psycopg2


app = Flask(__name__)

load_dotenv()
app = Flask(__name__)
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


if __name__ == "__main__":
    app.run(debug=True)
