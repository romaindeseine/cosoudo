from flask import current_app
from flask_login import UserMixin

from . import bcrypt, db, login_manager


class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
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
    id = db.Column(db.Integer, primary_key=True)
    doctorant = db.Column(db.String(64))
    date = db.Column(db.Date)
    donations = db.relationship('Donation', backref='soutenance')

    def to_json(self):
        return {
            'id': self.id,
            'doctorant': self.doctorant,
            'date': self.date,
            'donations': [donation.to_json() for donation in self.donations]
        }

    def __repr__(self):
        return '<Soutenance {}>'.format(self.doctorant)


class Donation(db.Model):
    __tablename__ = 'donations'
    id = db.Column(db.Integer, primary_key=True)
    donateur = db.Column(db.String(64))
    don = db.Column(db.Float)
    is_settled = db.Column(db.Boolean, default=False)
    soutenance_id = db.Column(db.Integer, db.ForeignKey('soutenances.id'))

    def to_json(self):
        return {
            'id': self.id,
            'donateur': self.donateur,
            'don': self.don,
            'is_settled': self.is_settled
        }

    def __repr__(self):
        return '<Donation {} - {}¢>'.format(self.donateur, self.don)
