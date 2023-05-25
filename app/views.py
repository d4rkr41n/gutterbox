from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import select
from app.models import target
from sqlalchemy import func
from app import app, db

@app.route('/', methods=['GET'])
def get_home():
    """Render website's home page."""
    targets = db.session.query(target).all()
    return render_template('home.html', targets=targets)

@app.route('/', methods=['POST'])
def post_home():
    """Render website's home page with applied filters."""
    targets = db.session.query(target)

    clientId = request.form.get("clientId")
    clientId = "default" if len(clientId) == 0 else clientId
    if clientId:
        targets = targets.where(target.clientId == clientId)

    os = request.form.get("os")
    if os:
        targets = targets.where(target.os == os)

    hostname = request.form.get("hostname")
    if hostname:
        targets = targets.filter(target.hostname.like('%'+hostname+'%'))

    address = request.form.get("address")
    if address:
        targets = targets.filter(target.address.like('%'+address+'%'))

    ports = request.form.get("ports")
    if ports:
        for port in ports.replace(' ','').split(','):
            targets = targets.filter(target.ports.like('%|'+port+'|%'))


    return render_template('home.html', targets=targets.all(), os=os,hostname=hostname,address=address,ports=ports,clientId=clientId)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
