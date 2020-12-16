from flask_wtf import FlaskForm

from wtforms import DecimalField, StringField, SubmitField
from wtforms.validators import DataRequired


class DonationForm(FlaskForm):
    donateur = StringField('Votre nom et prénom', validators=[DataRequired()])
    don = DecimalField('Hauteur du don', validators=[DataRequired()])
    submit = SubmitField('Submit')
