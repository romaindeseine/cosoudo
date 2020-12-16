import os

from dotenv import load_dotenv

from app import create_app, db
from app.models import Donation, Soutenance

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Donation=Donation, Soutenance=Soutenance)
