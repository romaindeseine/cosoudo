from flask_wtf import FlaskForm

from wtforms import (
    BooleanField,
    DateField,
    DecimalField,
    PasswordField,
    StringField,
    SubmitField
)
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
    donateur = StringField('Nom et prénom', validators=[DataRequired()])
    don = DecimalField('Hauteur du don', validators=[DataRequired()])
    is_settled = BooleanField('Dette réglée', default=False)
    submit = SubmitField('Submit')


class CadeauForm(FlaskForm):
    auteur = StringField('Nom et prénom', validators=[DataRequired()])
    idee = StringField('Idée', validators=[DataRequired()])
    submit = SubmitField('Submit')
