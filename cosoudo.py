import os

from flask_migrate import Migrate, upgrade

from dotenv import load_dotenv

from app import create_app, db
from app.models import Admin, Donation, Soutenance

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Admin=Admin, Donation=Donation, Soutenance=Soutenance)


@app.cli.command()
def deploy():
    # migre la base de donnée vers sa dernière version
    upgrade()

    # crée un administrateur
    Admin.create()
