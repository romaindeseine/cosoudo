from uuid import uuid4

from flask import current_app
from flask_login import UserMixin

from . import bcrypt, db, login_manager


def get_uuid():
    return uuid4().hex


class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.String(32), primary_key=True, default=get_uuid)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(64))

    @staticmethod
    def create():
        if not Admin.query.filter_by(email=current_app.config['ADMIN_EMAIL']).first():
            admin = Admin(
                email=current_app.config['ADMIN_EMAIL'],
                password=current_app.config['ADMIN_PASSWORD']
            )
            db.session.add(admin)
            db.session.commit()

    @property
    def password(self):
        raise AttributeError('password is not a readable attibute.')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(id):
    return Admin.query.get(id)


class Soutenance(db.Model):
    __tablename__ = 'soutenances'
    id = db.Column(db.String(32), primary_key=True, default=get_uuid)
    doctorant = db.Column(db.String(64))
    date = db.Column(db.Date)
    donations = db.relationship('Donation', backref='soutenance')
    cadeaux = db.relationship('Cadeau', backref='soutenance')

    def to_json(self):
        return {
            'id': self.id,
            'doctorant': self.doctorant,
            'date': self.date,
            'donations': [donation.to_json() for donation in self.donations],
            'cadeaux': [cadeau.to_json() for cadeau in self.cadeaux]
        }

    def __repr__(self):
        return '<Soutenance {}>'.format(self.doctorant)


class Donation(db.Model):
    __tablename__ = 'donations'
    id = db.Column(db.String(32), primary_key=True, default=get_uuid)
    donateur = db.Column(db.String(64))
    don = db.Column(db.Float)
    is_settled = db.Column(db.Boolean, default=False)
    soutenance_id = db.Column(db.String(32), db.ForeignKey('soutenances.id'))

    def to_json(self):
        return {
            'id': self.id,
            'donateur': self.donateur,
            'don': self.don,
            'is_settled': self.is_settled
        }

    def __repr__(self):
        return '<Donation {} - {}¢>'.format(self.donateur, self.don)


class Cadeau(db.Model):
    __tablename__ = 'cadeaux'
    id = db.Column(db.String(32), primary_key=True, default=get_uuid)
    auteur = db.Column(db.String(64))
    idee = db.Column(db.String(128))
    soutenance_id = db.Column(db.String(32), db.ForeignKey('soutenances.id'))

    def to_json(self):
        return {
            'id': self.id,
            'auteur': self.auteur,
            'idee': self.idee
        }
