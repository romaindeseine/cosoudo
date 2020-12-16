from flask import Blueprint, render_template

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


@main.route('/donation/<slug>', methods=['GET', 'POST'])
def donation(slug):
    return render_template('donation.html'), 200
