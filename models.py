from webapp.app import db

class Carton(db.Model):
    __tablename__ = 'carton'
    id = db.Column(db.Integer, primary_key=True, nullable = False, autoincrement = True)
    client = db.Column(db.String(20))
    oras = db.Column(db.String(20))
    dimensiune = db.Column(db.String(10))
    stampila = db.Column(db.String(10))
    stanta = db.Column(db.String(10))
    notite = db.Column(db.Text)
    culoare1_id = db.Column(db.Integer, db.ForeignKey('color.id'))
    culoare1 = db.relationship('Color', foreign_keys = [culoare1_id], lazy = True, backref = 'cul1')
    culoare2_id = db.Column(db.Integer, db.ForeignKey('color.id'))
    culoare2 = db.relationship('Color', foreign_keys = [culoare2_id], lazy = True, backref = 'cul2')


class Color(db.Model):
    __tablename__ = 'color'
    id = db.Column(db.Integer, primary_key=True, nullable = False, autoincrement = True)
    nume = db.Column(db.String(20))
    def __init__ (self, nume):
        self.nume = nume

class Emba(db.Model):
    tablename = 'emba'
    id = db.Column(db.Integer, primary_key = True,autoincrement = True, nullable = False)
    color_id = db.Column(db.Integer, db.ForeignKey('color.id'))
    embac = db.relationship('Color', foreign_keys = [color_id], backref = 'embacant')
    cant1 = db.Column(db.Float)
    cant2 = db.Column(db.Float)

class Simca(db.Model):
    tablename = 'simca'
    id = db.Column(db.Integer, primary_key = True,autoincrement = True, nullable = False)
    color_id = db.Column(db.Integer, db.ForeignKey('color.id'))
    simcac = db.relationship('Color', foreign_keys = [color_id], backref = 'simcacant')
    cant1 = db.Column(db.Float)
    cant2 = db.Column(db.Float)