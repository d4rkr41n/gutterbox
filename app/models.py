from app import db

class target(db.Model):
    __tablename__ = "targets"
    id = db.Column(db.Integer, primary_key = True)
    os = db.Column(db.String())
    hostname = db.Column(db.String())
    address = db.Column(db.String())
    ports = db.Column(db.String())
    clientId = db.Column(db.String())

    def __init__(self, os, hostname, address, ports, clientId):
        self.os = os
        self.hostname = hostname
        self.address = address
        self.ports = ports
        self.clientId = clientId

    def __repr__(self):
        return '<address %r>' % self.address
