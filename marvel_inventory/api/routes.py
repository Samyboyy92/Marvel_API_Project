from flask import Blueprint, request, jsonify
from marvel_inventory.helpers import token_required, random_jokes_generator
from marvel_inventory.models import db, Hero, hero_schema, heros_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/heros', methods = ['POST'])
@token_required
def create_hero(our_user):
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    date_created = request.json['date_created']
    random_jokes = random_jokes_generator()
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    hero = Hero(name, description, comics_appeared_in, super_power, date_created, random_jokes, user_token)

    db.session.add(hero)
    db.session.commit()

    response = hero_schema.dump(hero)

    return jsonify(response)

@api.route('/heros/<id>', methods = ['GET'])
@token_required
def get_hero(our_user, id):
    if id:
        hero = Hero.query.get(id)
        response = hero_schema.dump(hero)
        return jsonify(response)
    else:
        return jsonify({'message': 'ID is missing'}), 401

@api.route('/heros', methods = ['GET'])
@token_required
def get_heros(our_user):
    token = our_user.token
    heros = Hero.query.filter_by(user_token = token).all()
    response = heros_schema.dump(heros)

    return jsonify(response)

@api.route('/heros/<id>', methods = ['PUT'])
@token_required
def update_hero(our_user,id):
    hero = Hero.query.get(id)

    hero.name = request.json['name']
    hero.description = request.json['description']
    hero.comics_appeared_in = request.json['comics_appeared_in']
    hero.super_power = request.json['super_power']
    hero.date_created = request.json['date_created']
    hero.random_jokes = random_jokes_generator()
    hero.user_token = our_user.token

    db.session.commit()

    response = hero_schema.dump(hero)

    return jsonify(response)

@api.route('/heros/<id>', methods = ['Delete'])
@token_required
def delete_hero(our_user, id):
    hero = Hero.query.get(id)
    db.session.delete(hero)
    db.session.commit()

    response = hero_schema.dump(hero)    

    return jsonify(response)