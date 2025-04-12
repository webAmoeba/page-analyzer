from flask import render_template, request, flash, redirect, url_for
from page_analyzer.models import url as url_model


def index():
    urls = url_model.get_all()
    return render_template('urls.html', urls=urls)


def show(id):
    url_data = url_model.get_by_id(id)
    if not url_data:
        flash('URL не найден', 'danger')
        return redirect(url_for('urls'))
    return render_template('one_url.html', url=url_data)


def create():
    if request.method == "POST":
        url = request.form["url"]

        errors = url_model.validate(url)
        if errors:
            flash(errors[0], 'danger')
            return render_template('index.html')

        if url_model.exists(url):
            flash('Страница уже существует', 'info')
            return render_template('index.html')

        url_model.create(url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('urls'))
    return render_template('index.html')
