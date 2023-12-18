from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "name": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


# PLANETS

class Planet (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(240))
    population = db.Column(db.Integer)
    clima = db.Column(db.String(120))

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id" : self.id,
            "name": self.name,
            "description": self.description,
            "population": self.population,
            "clima": self.clima
        }
    
# CHARACTERS

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120))
    hair_color = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(240))

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id" : self.id,
            "name": self.name,
            "hair_color": self.hair_color,
            "description": self.description,
            "gender": self.gender
        }
    
# VEHICLES

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    model = db.Column(db.String(120))
    

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id" : self.id,
            "name": self.name,
            "model": self.model
        }

#  FAVORITES
 
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)

    planet = db.relationship('Planet')
    character = db.relationship('Character')
    user = db.relationship('User')

    def __repr__(self):
        return f'<Favorite {self.id} >'

    def serialize(self):
        return {
            'id': self.id,
            'planet': self.planet.serialize() if self.planet else None,
            'character': self.character.serialize() if self.character else None
        }