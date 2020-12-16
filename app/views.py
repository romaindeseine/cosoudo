from flask import Blueprint, render_template

from .forms import DonationForm

main = Blueprint('main', __name__)


@main.route('/')
def home():
    soutenances = [
        'Pierre Boutaud',
        'Romain Deseine',
        'Cyril Falcon',
        'Hugo Federico'
    ]
    return render_template('home.html', soutenances=soutenances), 200


@main.route('/donation/<id>', methods=['GET', 'POST'])
def donation(id):
    form = DonationForm()
    if form.validate_on_submit():
        don = form.don.data
        print(don)
    return render_template('donation.html', form=form, soutenance='Pierre Boutaud'), 200
