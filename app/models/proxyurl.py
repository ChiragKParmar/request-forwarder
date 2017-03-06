from .. import db

class ProxyUrl(db.Model):
    __tablename__ = 'proxy'
    id = db.Column(db.Integer, primary_key=True)
    incoming_url = db.Column(db.String(64), unique=True)
    outgoing_url = db.Column(db.String(64))

    def __repr__(self):
        return '<ProxyUrl %r>' % self.incoming_url
