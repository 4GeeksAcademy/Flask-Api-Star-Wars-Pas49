"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

logged_user_id = 1

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_all_users():
    allUsers = User.query.all()

    response_body = list(map(lambda item: item.serialize(), allUsers))


    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

# PEOPLE ROUTES
    
@app.route('/people', methods=['GET'])
def get_all_characters():
    allCharacters = Character.query.all()

    result = list(map(lambda item: item.serialize(), allCharacters))

    return jsonify(result), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):

    character = Character.query.get(people_id)

    result = character.serialize()

    return jsonify(result), 200

# PLANET ROUTES 

@app.route('/planets', methods=['GET'])
def get_all_planets():
    allPlanets = Planet.query.all()

    result = list(map(lambda item: item.serialize(), allPlanets))


    return jsonify(result), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):

    planet = Planet.query.get(planet_id)

    result = planet.serialize()

    return jsonify(result), 200

    # FAVORITES ROUTES 

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):

     new_favorite = Favorite(user_id=logged_user_id, planet_id=planet_id)
     
     db.session.add(new_favorite)
     db.session.commit()

     response_body = { 
        "favorite": new_favorite.serialize()
    }

     return jsonify(response_body), 200


@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):

    new_favorite = Favorite(user_id=logged_user_id, character_id = character_id)
    db.session.add(new_favorite)
    db.session.commit()

    response_body = {
        "favorite": new_favorite.serialize()
    }

    return jsonify(response_body), 200


@app.route('/users/favorites', methods=['GET'])
def get_all_favorites():

    favorites = Favorite.query.all()

    result = list(map(lambda item: item.serialize(), favorites))

    return jsonify(result), 200



@app.route('/favorite/character/<int:favorite_id>', methods=['DELETE'])
def delete_favorite_character(favorite_id):
    
    favorite = Favorite.query.get(favorite_id)

    if favorite is None:
        return jsonify({'msg' : 'No favorite found'}), 404
    
    db.session.delete(favorite)
    db.session.commit()

    response_body = {
        "msg" : "Favorite Character Removed"
    }
    return jsonify(response_body), 200



@app.route('/favorite/planet/<int:favorite_id>', methods=['DELETE'])
def delete_favorite_planet(favorite_id):
    
    favorite = Favorite.query.get(favorite_id)

    if favorite is None:
        return jsonify({'msg' : 'No favorite found'}), 404
    
    db.session.delete(favorite)
    db.session.commit()

    response_body = {
        "msg" : "Favorite Planet Removed"
    }
    return jsonify(response_body), 200