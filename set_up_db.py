from app import create_app
from extensions import db
from models import User

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Database and tables created successfully!")
