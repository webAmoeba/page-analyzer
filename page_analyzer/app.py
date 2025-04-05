from flask import Flask, render_template
from dotenv import load_dotenv
import os
import psycopg2


app = Flask(__name__)

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/urls")
def urls():
    return render_template('urls.html')


if __name__ == "__main__":
    app.run(debug=True)
