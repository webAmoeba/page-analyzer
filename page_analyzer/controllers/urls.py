from flask import render_template, request, flash, redirect, url_for, abort
from page_analyzer.models import url as url_model
from page_analyzer.models import url_check as check_model


def index():
    urls = url_model.get_all_with_latest_check()
    return render_template('urls.html', urls=urls)


def show(id):
    url_data = url_model.get_by_id(id)
    if not url_data:
        abort(404)

    checks = check_model.get_checks_for_url(id)

    return render_template('one_url.html', url=url_data, checks=checks)


def check(id):
    url_data = url_model.get_by_id(id)
    if not url_data:
        abort(404)

    check_result = check_model.create(id, url_data['name'])

    if check_result is None:
        flash('Произошла ошибка при проверке', 'danger')
    else:
        flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_one_url', id=id))


def create():
    if request.method == "POST":
        url = request.form["url"]

        errors = url_model.validate(url)
        if errors:
            flash(errors[0], 'danger')
            return redirect(url_for('home'))

        if url_model.exists(url):
            flash('Страница уже существует', 'info')
            return redirect(url_for('home'))

        url_id = url_model.create(url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('get_one_url', id=url_id))
    return render_template('index.html')
