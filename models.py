from extensions import db

class User(db.Model):
    __tablename__ = 'users'  # better to be explicit
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password= db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'
