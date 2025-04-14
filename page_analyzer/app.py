from flask import Flask, render_template
from dotenv import load_dotenv
from page_analyzer.controllers import urls as urls_controller
import os

app = Flask(__name__)
load_dotenv()

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


# Routes
@app.route("/", methods=["GET", "POST"])
def home():
    return urls_controller.create()


@app.route("/urls")
def urls():
    return urls_controller.index()


@app.route("/urls/<id>")
def get_one_url(id):
    return urls_controller.show(id)


@app.route("/urls/<id>/checks", methods=['POST'])
def check_url(id):
    return urls_controller.check(id)


@app.errorhandler(404)
def page_not_found(_):
    return render_template('404.html'), 404


@app.template_filter("dateformat")
def dateformat(date):
    return date.strftime("%Y-%m-%d")


if __name__ == "__main__":
    app.run(debug=True)
