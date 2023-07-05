from flask import request, jsonify
from functools import wraps
import secrets
import decimal
import requests
import json

from marvel_inventory.models import User



def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):

        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split()[1]
            print(token)

        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            our_user = User.query.filter_by(token=token).first()
            print(our_user)
            if not our_user or our_user.token != token:
                return jsonify({'message': 'Token is invalid'}), 401
            
        except:
            our_user = User.query.filter_by(token=token).first()
            if token != our_user.token and secrets.compare_digest(token, our_user.token):
                return jsonify({'message': 'Token is invalid'}), 401
        return our_flask_function(our_user, *args, **kwargs)
    return decorated

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return json.JSONEncoder(JSONEncoder, self).default(obj)

def random_jokes_generator():
    url = "https://humor-jokes-and-memes.p.rapidapi.com/jokes/random"

    querystring = {"max-length":"200","include-tags":"one_liner","min-rating":"7","exclude-tags":"nsfw","keywords":"rocket"}

    headers = {
        "X-RapidAPI-Key": "a4f38f9b2dmsh45db4d65d4caaa8p180fe4jsn22deef91a361",
        "X-RapidAPI-Host": "humor-jokes-and-memes.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()

    return data['joke']