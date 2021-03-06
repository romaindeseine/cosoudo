from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import db
from .forms import CadeauForm, DonationForm, LoginForm, SoutenanceForm
from .models import Admin, Cadeau, Donation, Soutenance

main = Blueprint("main", __name__)


@main.route("/")
def home():
    soutenances = Soutenance.query.all()
    return render_template("home.html", soutenances=soutenances), 200


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin is not None and admin.verify_password(form.password.data):
            login_user(admin)
            flash(
                message="Vous avez bien réussi à vous connecter au site de la CoSouDo.",
                category="success",
            )
            return redirect(url_for("main.home"))
        else:
            flash("Mauvais email ou mot de passe.", category="danger")

    return render_template("login.html", form=form), 200


@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash(
        message="Vous avez bien été déconnecté du site de la CoSouDo.",
        category="success",
    )
    return redirect(url_for("main.home"))


@main.route("/soutenances", methods=["GET"])
@login_required
def voir_soutenances():
    soutenances = [soutenance.to_json() for soutenance in Soutenance.query.all()]
    for soutenance in soutenances:
        soutenance["cagnotte"] = 0
        soutenance["is_settled"] = True
        for donation in soutenance["donations"]:
            soutenance["cagnotte"] += donation["don"]
            if not donation["is_settled"]:
                soutenance["is_settled"] = False

    return render_template("soutenances.html", soutenances=soutenances), 200


@main.route("/soutenances/nouvelle", methods=["GET", "POST"])
@login_required
def nouvelle_soutenance():
    form = SoutenanceForm()

    if form.validate_on_submit():
        soutenance = {key: form[key].data for key in ["doctorant", "date"]}
        db.session.add(Soutenance(**soutenance))
        db.session.commit()
        flash(
            message="La soutenance de {} a bien été ajoutée. "
            "Il faut maintenant récolter les sousous.".format(soutenance["doctorant"]),
            category="success",
        )
        return redirect(url_for("main.voir_soutenances"))

    return render_template("nouvelle_soutenance.html", form=form), 200


@main.route("/soutenances/<id>/supprimer", methods=["POST"])
@login_required
def supprimer_soutenance(id):
    """
    :param id: Id de la soutenance
    """
    soutenance = Soutenance.query.get_or_404(id)
    db.session.delete(soutenance)
    db.session.commit()
    flash(
        message="La soutenance de {} a bien été supprimée.".format(
            soutenance.doctorant
        ),
        category="success",
    )
    return redirect(url_for("main.voir_soutenances"))


@main.route("/soutenance/<id>/modifier", methods=["GET", "POST"])
@login_required
def modifier_soutenance(id):
    """
    :param id: Id de la soutenance
    """
    soutenance = Soutenance.query.get_or_404(id)
    form = SoutenanceForm()

    if form.validate_on_submit():
        soutenance.doctorant = form.doctorant.data
        soutenance.date = form.date.data
        db.session.add(soutenance)
        db.session.commit()
        flash(
            message="La soutenance de {} a bien été modifiée.".format(
                soutenance.doctorant
            ),
            category="success",
        )
        return redirect(url_for("main.voir_soutenances"))

    form.doctorant.data = soutenance.doctorant
    form.date.data = soutenance.date
    return render_template("modifier_soutenance.html", form=form, soutenance=soutenance)


@main.route("/soutenances/<id>/donation_ou_cadeau")
def donation_ou_cadeau(id):
    """
    :param id: Id de la soutenance
    """
    soutenance = Soutenance.query.get_or_404(id)
    return render_template("donation_ou_cadeau.html", soutenance=soutenance)


@main.route("/soutenance/<id>/dons", methods=["GET"])
@login_required
def voir_donations_soutenance(id):
    """
    :param id: Id de la soutenance
    """
    soutenance = Soutenance.query.get_or_404(id)
    return (
        render_template("donations_soutenance.html", soutenance=soutenance.to_json()),
        200,
    )


@main.route("/soutenances/<id>/donations/nouvelle", methods=["GET", "POST"])
def nouvelle_donation(id):
    """
    :param id: Id de la soutenance
    """
    soutenance = Soutenance.query.get_or_404(id)
    form = DonationForm()

    if form.validate_on_submit():
        donation = {key: form[key].data for key in ["donateur", "don"]}
        donation["soutenance_id"] = id
        db.session.add(Donation(**donation))
        db.session.commit()
        flash(
            message="Ta participation a bien été ajoutée. La CoSouDo te remercie.",
            category="success",
        )
        return redirect(url_for("main.home"))

    return (
        render_template(
            "nouvelle_donation.html", form=form, doctorant=soutenance.doctorant
        ),
        200,
    )


@main.route("/donations/<id>/supprimer", methods=["POST"])
@login_required
def supprimer_donation(id):
    """
    :param id: Id de la donation
    """
    donation = Donation.query.get_or_404(id)
    db.session.delete(donation)
    db.session.commit()
    flash(
        message="La donation de {} a bien été supprimée.".format(donation.donateur),
        category="success",
    )
    return redirect(
        url_for("main.voir_donations_soutenance", id=donation.soutenance_id)
    )


@main.route("/donations/<id>/modifier", methods=["GET", "POST"])
@login_required
def modifier_donation(id):
    """
    :param id: Id de la donation
    """
    donation = Donation.query.get_or_404(id)
    form = DonationForm()

    if form.validate_on_submit():
        donation.donateur = form.donateur.data
        donation.don = form.don.data
        donation.is_settled = form.is_settled.data
        db.session.add(donation)
        db.session.commit()
        flash(
            message="La donation de {} a bien été modifée.".format(donation.donateur),
            category="success",
        )
        return redirect(
            url_for("main.voir_donations_soutenance", id=donation.soutenance_id)
        )

    form.donateur.data = donation.donateur
    form.don.data = donation.don
    form.is_settled.data = donation.is_settled
    return render_template("modifier_donation.html", form=form, donation=donation)


@main.route("/soutenance/<id>/cadeaux", methods=["GET"])
@login_required
def voir_cadeaux_soutenance(id):
    """
    :param id: Id de la soutenance
    """
    soutenance = Soutenance.query.get_or_404(id)
    return (
        render_template("cadeaux_soutenance.html", soutenance=soutenance.to_json()),
        200,
    )


@main.route("/soutenances/<id>/cadeaux/nouveau", methods=["GET", "POST"])
def nouveau_cadeau(id):
    """
    :param id: Id de la soutenance
    """
    soutenance = Soutenance.query.get_or_404(id)
    form = CadeauForm()

    if form.validate_on_submit():
        cadeau = {key: form[key].data for key in ["auteur", "idee"]}
        cadeau["soutenance_id"] = id
        db.session.add(Cadeau(**cadeau))
        db.session.commit()
        flash(
            message="Ton idée de cadeau a bien été ajoutée. La CoSouDo te remercie.",
            category="success",
        )
        return redirect(url_for("main.home"))

    return (
        render_template(
            "nouveau_cadeau.html", form=form, doctorant=soutenance.doctorant
        ),
        200,
    )


@main.route("/cadeaux/<id>/supprimer", methods=["POST"])
@login_required
def supprimer_cadeau(id):
    """
    :param id: Id du cadeau
    """
    cadeau = Cadeau.query.get_or_404(id)
    db.session.delete(cadeau)
    db.session.commit()
    flash(
        message="L'idée de cadeau de {} a bien été supprimée".format(cadeau.auteur),
        category="success",
    )
    return redirect(url_for("main.voir_cadeaux_soutenance", id=cadeau.soutenance_id))


@main.route("/cadeaux/<id>/modifier", methods=["GET", "POST"])
@login_required
def modifier_cadeau(id):
    """
    :param id: Id du cadeau
    """
    cadeau = Cadeau.query.get_or_404(id)
    form = CadeauForm()

    if form.validate_on_submit():
        cadeau.auteur = form.auteur.data
        cadeau.idee = form.idee.data
        db.session.add(cadeau)
        db.session.commit()
        flash(
            message="L'idée de cadeau de {} a bien été modifée.".format(cadeau.auteur),
            category="success",
        )
        return redirect(
            url_for("main.voir_cadeaux_soutenance", id=cadeau.soutenance_id)
        )

    form.auteur.data = cadeau.auteur
    form.idee.data = cadeau.idee
    return render_template("modifier_cadeau.html", form=form, cadeau=cadeau)
