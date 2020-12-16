from flask_wtf import FlaskForm

from wtforms import DateField, DecimalField, StringField, SubmitField
from wtforms.validators import DataRequired


class SoutenanceForm(FlaskForm):
    doctorant = StringField('Nom et prénom du doctorant', validators=[DataRequired()])
    date = DateField('Date de la soutenance', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DonationForm(FlaskForm):
    donateur = StringField('Votre nom et prénom', validators=[DataRequired()])
    don = DecimalField('Hauteur du don', validators=[DataRequired()])
    submit = SubmitField('Submit')
