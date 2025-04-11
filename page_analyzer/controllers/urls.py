from flask import render_template, request
from page_analyzer.models import url as url_model


def index():
    urls = url_model.get_all()
    return render_template('urls.html', urls=urls)


def show(id):
    url_data = url_model.get_by_id(id)
    if not url_data:
        return render_template('one_url.html', error='URL не найден')
    return render_template('one_url.html', url=url_data)


def create():
    if request.method == "POST":
        url = request.form["url"]

        errors = url_model.validate(url)
        if errors:
            return render_template('index.html', message=errors[0])

        if url_model.exists(url):
            return render_template(
                'index.html',
                message='Страница уже существует'
            )

        url_model.create(url)
        return render_template(
            'index.html',
            message='Страница успешно добавлена'
        )
    return render_template('index.html')
