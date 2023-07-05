from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from marvel_inventory.forms import MarvelForm
from marvel_inventory.models import Hero, db
from marvel_inventory.helpers import random_jokes_generator

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    print('Marvel is better than DC')
    return render_template('index.html')

@site.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    marvelform = MarvelForm()
    try:
        if request.method == 'POST' and marvelform.validate_on_submit():
            name = marvelform.name.data
            description = marvelform.description.data
            comics_appeared_in = marvelform.comics_appeared_in.data
            super_power = marvelform.super_power.data
            date_created = marvelform.date_created.data
            if marvelform.random_jokes.data:
                random_jokes = marvelform.random_jokes.data
            else:
                random_jokes = random_jokes_generator()
            user_token = current_user.token
            
            hero = Hero(name, description, comics_appeared_in, super_power, date_created, random_jokes, user_token)

            db.session.add(hero)
            db.session.commit()

            return redirect(url_for('site.profile'))
        
    except:
        raise Exception('Hero was not created, please check your form and try again')
    
    user_token = current_user.token
    heros = Hero.query.filter_by(user_token=user_token)

    return render_template('profile.html', form=marvelform, heros=heros) 








