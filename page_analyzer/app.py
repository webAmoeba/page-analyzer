from flask import Flask
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/")
def home():
    return "Welcome to the Page Analyzer!"


if __name__ == "__main__":
    app.run(debug=True)
