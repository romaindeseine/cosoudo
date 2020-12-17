from flask import Blueprint, flash, redirect, render_template, url_for

from . import db
from .forms import DonationForm, SoutenanceForm
from .models import Donation, Soutenance

main = Blueprint('main', __name__)


@main.route('/')
def home():
    soutenances = Soutenance.query.all()
    return render_template('home.html', soutenances=soutenances), 200


@main.route('/donation/<id>', methods=['GET', 'POST'])
def donation(id):
    """
    :param id: Id de la soutenance
    """
    soutenance = Soutenance.query.get_or_404(id)
    form = DonationForm()

    if form.validate_on_submit():
        donation = {key: form[key].data for key in ['donateur', 'don']}
        donation['soutenance_id'] = id
        db.session.add(Donation(**donation))
        db.session.commit()
        flash(
            message='Ta participation a bien été ajoutée. La CoSouDo te remercie.',
            category='success'
        )
        return redirect(url_for('main.home'))

    return render_template(
        'donation.html', form=form, doctorant=soutenance.doctorant
    ), 200


@main.route('/soutenances', methods=['GET'])
def get_soutenances():
    soutenances = [soutenance.to_json() for soutenance in Soutenance.query.all()]
    for soutenance in soutenances:
        soutenance['cagnotte'] = 0
        soutenance['is_settled'] = True
        for donation in soutenance['donations']:
            soutenance['cagnotte'] += donation['don']
            if not donation['is_settled']:
                soutenance['is_settled'] = False

    return render_template('soutenances.html', soutenances=soutenances), 200


@main.route('/soutenances/nouvelle', methods=['GET', 'POST'])
def nouvelle_soutenance():
    form = SoutenanceForm()

    if form.validate_on_submit():
        soutenance = {key: form[key].data for key in ['doctorant', 'date']}
        db.session.add(Soutenance(**soutenance))
        db.session.commit()
        flash(
            message='La soutenance a bien été ajoutée. '
            'Il faut maintenant récolter les sousous.',
            category='success'
        )
        return redirect(url_for('main.home'))

    return render_template('nouvelle_soutenance.html', form=form), 200
