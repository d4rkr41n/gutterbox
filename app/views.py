from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import select
from app.models import target
from sqlalchemy import func
from sqlalchemy import or_, not_
from app import app, db


def targets_filter(targets, column, terms):
    # Re-Usable Filtering For Columns, implicit AND with || operator support
    conditions = []
    for item in terms.replace(' ','').split(','):
        for item_or in item.split('||'):
            if item_or.startswith('!'):
                conditions.append( not_(column.ilike(item_or.replace('!','') + '%')) )
            else:
                conditions.append( column.ilike(item_or.replace('!','') + '%') )
        targets = targets.filter(or_(*conditions))
    return targets

@app.route('/', methods=['GET'])
def get_home():
    """Render website's home page."""
    clientId = "default"
    targets = db.session.query(target)
    targets = targets.where(target.clientId == clientId)
    return render_template('home.html', targets=targets.all(), clientId=clientId)

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
        targets = targets_filter(targets, target.os, os)

    hostname = request.form.get("hostname")
    if hostname:
        targets = targets_filter(targets, target.hostname, hostname)

    address = request.form.get("address")
    if address:
        targets = targets_filter(targets, target.address, address)

    ports = request.form.get("ports")
    if ports:
        # I needed a non-default case to handle ports since they have a | separator in the DB
        conditions = []
        for item in ports.replace(' ','').split(','):
            for item_or in item.split('||'):
                if item_or.startswith('!'):
                    conditions.append( not_(target.ports.ilike('%|' + item_or.replace('!','') + '|%')) )
                else:
                    conditions.append( target.ports.ilike('%|' + item_or.replace('!','') + '|%') )
            targets = targets.filter(or_(*conditions))

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
