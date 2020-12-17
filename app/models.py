from . import db


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
