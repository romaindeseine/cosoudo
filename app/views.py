from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import db
from .forms import DonationForm, LoginForm, SoutenanceForm
from .models import Admin, Donation, Soutenance

main = Blueprint('main', __name__)


@main.route('/')
def home():
    soutenances = Soutenance.query.all()
    return render_template('home.html', soutenances=soutenances), 200


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin is not None and admin.verify_password(form.password.data):
            login_user(admin)
            flash(
                message='Vous avez bien réussi à vous connecter au site de la CoSouDo.',
                category='success'
            )
            return redirect(url_for('main.home'))
        else:
            flash('Mauvais email ou mot de passe.', category='danger')

    return render_template('login.html', form=form), 200


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash(
        message='Vous avez bien été déconnecté du site de la CoSouDo.',
        category='success'
    )
    return redirect(url_for('main.home'))


@main.route('/soutenances/<id>/donations', methods=['GET', 'POST'])
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
@login_required
def voir_soutenances():
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
@login_required
def nouvelle_soutenance():
    form = SoutenanceForm()

    if form.validate_on_submit():
        soutenance = {key: form[key].data for key in ['doctorant', 'date']}
        db.session.add(Soutenance(**soutenance))
        db.session.commit()
        flash(
            message='La soutenance de {} a bien été ajoutée. '
            'Il faut maintenant récolter les sousous.'.format(
                soutenance['doctorant']
            ),
            category='success'
        )
        return redirect(url_for('main.home'))

    return render_template('nouvelle_soutenance.html', form=form), 200


@main.route('/soutenance/<id>', methods=['GET'])
@login_required
def voir_soutenance(id):
    """
    :param id: Id de la soutenance
    """
    soutenance = Soutenance.query.get_or_404(id)
    return render_template('soutenance.html', soutenance=soutenance.to_json()), 200


@main.route('/soutenance/<id>/supprimer', methods=['POST'])
@login_required
def supprimer_soutenance(id):
    """
    :param id: Id de la soutenance
    """
    soutenance = Soutenance.query.get_or_404(id)
    db.session.delete(soutenance)
    db.session.commit()
    flash(
        message='La soutenance de {} a bien été supprimée.'.format(
            soutenance.doctorant
        ),
        category='success'
    )
    return redirect(url_for('main.home'))
