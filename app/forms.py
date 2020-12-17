from flask_wtf import FlaskForm

from wtforms import DateField, DecimalField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SoutenanceForm(FlaskForm):
    doctorant = StringField('Nom et prénom du doctorant', validators=[DataRequired()])
    date = DateField('Date de la soutenance', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DonationForm(FlaskForm):
    donateur = StringField('Votre nom et prénom', validators=[DataRequired()])
    don = DecimalField('Hauteur du don', validators=[DataRequired()])
    submit = SubmitField('Submit')
