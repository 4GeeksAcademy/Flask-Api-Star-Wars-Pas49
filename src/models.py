from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    height = db.Column(db.String(50), unique=False, nullable=True)
    hair_color = db.Column(db.String(50), unique=False, nullable=True)
    eye_color = db.Column(db.String(20), unique=False, nullable=True)
    birth_year = db.Column(db.String(20), unique=False, nullable=True)
    gender = db.Column(db.String(50), unique=False, nullable=True)
    

    def __repr__(self):
        return '<Characters %r>' % self.id


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }