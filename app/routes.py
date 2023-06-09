from app import app
from flask import render_template, request, redirect, url_for, Flask, jsonify, flash, session
import requests
from .models import Pokemon, User, Pokedex
from .forms import PokemonCatchForm 
from flask_login import  current_user
from sqlalchemy import select 

@app.route('/')
def homePage():
    greeting = "Welcome to my Pokemon app!"

    

    return render_template('index.html', greeting = greeting)

        
@app.route('/pokeform', methods=['GET', 'POST'])
def pokePicker():

    form = PokemonCatchForm()

    return render_template('pokeform.html', form = form)

@app.route('/my-pokemon', methods = ['GET', 'POST'])
def myPokemon():
    # my_pokemon = Pokemon.query.all()
    my_pokemon = Pokemon.query.filter(Pokemon.user_id == current_user.id).all()
    

    return render_template('pokedex.html', my_pokemon = my_pokemon)


@app.route('/pokedata', methods=['GET', 'POST'])
def pokedata():
    # print(request.form['pokemon_name'])
    my_pokemon = Pokemon.query.filter(Pokemon.user_id == current_user.id).all()

    if len(my_pokemon)+1 <= 5:
        print(my_pokemon)
        print('you can still catch more pokemon')
        pass
    else:
        print('your bag is full')
        message = flash("You already have 5 pokemon", category="danger")
        return redirect(url_for('myPokemon', message = message))
    
    if request.form != "":
        name = request.form["pokemon_name"].lower()
        # print(name)
        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        my_pkmn = {}
        response = requests.get(url)
    else:
        return jsonify({"error": "Pokemon not found."}), 404

    if response.status_code == 200 and name:
        pokemon = response.json()
        my_pkmn['Name'] = pokemon['name'].title()   
        my_pkmn['abilityName'] = pokemon['abilities'][0]['ability']['name'].title()
        my_pkmn['baseXP'] = pokemon['base_experience']
        my_pkmn['shiny'] = pokemon["sprites"]['front_shiny']
        my_pkmn['attack'] = pokemon['stats'][1]['base_stat']
        my_pkmn['hp'] = pokemon['stats'][0]['base_stat']
        my_pkmn['defense'] = pokemon['stats'][2]['base_stat']

        pokename = my_pkmn['Name']
        ability_name = my_pkmn['abilityName']
        base_xp = my_pkmn['baseXP']
        shiny = my_pkmn['shiny']
        attack = my_pkmn['attack']
        hp = my_pkmn['hp']
        defense = my_pkmn['defense']

        pokemon = Pokemon(pokename, ability_name, base_xp, shiny, attack, hp, defense, current_user.id) 
        pokemon.saveToDB()


        
        pokedex = Pokedex(current_user.id, pokemon.id)
        pokedex.saveToDB()

      # print(my_pkmn)
        return render_template('pokedisplay.html', my_pkmn = my_pkmn)
    else:
        return jsonify({"error": "Pokemon not found."}), 404


@app.route('/battlefield')
def battlefield():

    # my_pokemon = Pokemon.query.filter(Pokemon.user_id == current_user.id).all()

    all_users = User.query.all()


    home = Pokemon.query.filter(Pokemon.user_id == current_user.id).all()

    # rogelio817 = Pokemon.query.filter(Pokemon.user_id == 2).all()
    # bc = Pokemon.query.filter(Pokemon.user_id == 2).all()



    ## === BATTLE LOGIC ====
    # grab all of a user's pokemon stats via pokedex    
    # sum-total battling: add up all of a user's pokemon hp and defense, subtract attack: highest shield stat wins


    return render_template('battlefield.html', home = home, all_users = all_users)

@app.route('/choose_opponent/<int:user_id>')
def chooseOpponent(user_id):
    # u = int(user.id)
    print(user_id)

    opponents_pokemon = Pokemon.query.filter(Pokemon.user_id == user_id).all()

    opponent_id = user_id
    session['opponent_id'] = opponent_id
    #### HOW TO PASS THIS VARIABLE FROM THIS SCOPE TO battleOpponent SCOPE#####
    
    home = Pokemon.query.filter(Pokemon.user_id == current_user.id).all()

    #winner = math logic to determine winner
    #return redirect(url_for('battleOpponent', winner = winner)) 

    return render_template('battlefield.html', opponents_pokemon = opponents_pokemon, home = home)

@app.route('/battle_opponent/<opponents_pokemon>/<home>/', methods = ['GET', 'POST'])
def battleOpponent(home, opponents_pokemon):
    print('testing')
    print(home)
    print(opponents_pokemon)
    
    home = Pokemon.query.filter(Pokemon.user_id == current_user.id).all()

    opponent_id = session.get('opponent_id')
    opponents_pokemon = Pokemon.query.filter(Pokemon.user_id == opponent_id).all()

    ## PREP LOGIC ##

    home_attack = 0
    home_hp = 0
    home_defense = 0

    opponents_attack = 0
    opponents_hp = 0
    opponents_defense = 0

    for pokemon in home:
        # print(pokemon)
        home_hp += pokemon.hp
        home_defense += pokemon.defense
        home_attack += pokemon.attack
        home_shield = home_hp + home_attack
    
    print(f'H_SHIELD' + str(home_shield))
    print(f'H_ATTACK' + str(home_attack))

    for pokemon in opponents_pokemon:
        # print(pokemon)
        opponents_hp += pokemon.hp
        opponents_defense += pokemon.defense
        opponents_attack += pokemon.attack
        opponents_shield = opponents_hp + opponents_attack
    
    print(f'O_SHIELD: ' + str(opponents_shield))
    print(f'O_ATTACK: ' + str(opponents_attack))

    ## BATTLE LOGIC ##
    opponents_shield -= home_attack
    home_shield -= opponents_shield
    if home_shield > opponents_shield:
        winner = "HOME WINS!"
    elif opponents_shield > home_shield:
        winner = "OPPONENT WINS"
    else:
        winner = "TIE!"

    return render_template('battlefield.html', opponents_pokemon = opponents_pokemon, home = home, winner = winner)

@app.route('/pokemon/<int:pokemon_id>/delete', methods = ["GET"])
def deletePokemon(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    
    pokemon.deleteFromDB()

    return redirect(url_for('myPokemon'))
