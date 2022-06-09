import requests
import json
import random
# to translate any language action comment from API into English
# install googletrans via terminal first using 'pip install googletrans'
from googletrans import Translator
import datetime

# arbitrary initial amount of health points lps
health_points = 500


# function that start the game by randomly generating a first pokemon for the user
def begin_game():
    # generates random first pokemon for user
    random_user_pokemon = random.randint(1, 151)
    url = 'https://pokeapi.co/api/v2/pokemon/{}'.format(random_user_pokemon)
    response = requests.get(url).text
    first_user_pokemon = json.loads(response)
    # print name of specific pokemon in the list nested under 'results' key in response_info dictionary
    global pokemon_name
    pokemon_name = first_user_pokemon['name']
    print("Your first pokemon is " + pokemon_name + ". Its moves are: ")
    # print list of moves for pokemon from API
    for item in first_user_pokemon['moves']:
        print(item['move']['name'], end=', \n')
    # gives pokedex variable global scope, so it can be accessed within other functions
    global pokedex
    # generates dictionary of pokemon name (key) and API info (value)
    pokedex = {
        pokemon_name: first_user_pokemon
    }


# function to select new pokemon from API for battle
def next_pokemon_info():
    while True:
        try:
            next_pokemon_input = input("Who's your next champion? \n")
            url = 'https://pokeapi.co/api/v2/pokemon/{}'.format(next_pokemon_input)
            response = requests.get(url).text
            global next_pokemon
            next_pokemon = json.loads(response)
        # this is to avoid JSONDecodeError that showed up for any word that isn't recognised within the API
        # i.e. not the name of a pokemon
        except ValueError:
            print('This is not a valid choice. Please check spelling.')
            pokedex_view()
        # this only runs if the user types the correct name of a pokemon
        else:
            if next_pokemon_input in list(pokedex.keys()):
                print('You have chosen ' + next_pokemon_input + '. Its moves are:  \n')
                for item in next_pokemon['moves']:
                    print(item['move']['name'], end=', \n')
                break
            else:
                print('Select one of the cards in your pokedex \n')
                pokedex_view()


# generates random pokemon and a random one of its moves for enemy
def enemy_choice():
    random_enemy_pokemon = random.randint(1, 151)
    url1 = 'https://pokeapi.co/api/v2/pokemon/{}'.format(random_enemy_pokemon)
    response1 = requests.get(url1).text
    global enemy_pokemon
    enemy_pokemon = json.loads(response1)
    global enemy_name
    enemy_name = enemy_pokemon['name']
    print("Your enemy has chosen " + enemy_name + '\n')

    # generates random move from enemy's pokemon
    random_enemy_move = random.choice(enemy_pokemon['moves'])
    enemy_move = random_enemy_move['move']['name']
    print(enemy_name + " uses " + enemy_move + '\n')

    # retrieves info on enemy's move
    url2 = 'https://pokeapi.co/api/v2/move/{}'.format(enemy_move)
    response2 = requests.get(url2).text
    move_info = json.loads(response2)
    move_comment = move_info['flavor_text_entries'][0]['flavor_text']
    translation = Translator()
    translated_comment = translation.translate(move_comment)
    print(translated_comment.text + '\n')

    # shows stat of enemy move power
    global enemy_move_power
    enemy_move_power_info = move_info['power']
    enemy_move_power = int(0 if enemy_move_power_info is None else enemy_move_power_info)


# allows user to type in their choice of move and retrieves info for use in battle
def get_move():
    while True:
        global user_move_input
        user_move_input = input('\nWhat move would you like to use? \n')
        try:
            url2 = 'https://pokeapi.co/api/v2/move/{}'.format(user_move_input)
            response2 = requests.get(url2).text
            move_info1 = json.loads(response2)
            print('You have chosen ' + user_move_input + '\n')
            move_comment1 = move_info1['flavor_text_entries'][0]['flavor_text']
            translation = Translator()
            translated_comment1 = translation.translate(move_comment1)
            print(translated_comment1.text + '\n')
            global user_move_power
            user_move_power_info = move_info1['power']
            user_move_power = int(0 if user_move_power_info is None else user_move_power_info)
            print('Your power is: ' + str(user_move_power))
            break
        # ValueError exception to account for mispellings or random words input
        except ValueError:
            print('Please select a valid move from the list and check spelling.')


# function to start battle between pokemon. Who wins depends on higher power stat.
def battle():
    if user_move_power > enemy_move_power:
        global winner
        winner = 'User'
        print(enemy_name + ' is defeated. ')
        print('You have ' + str(health_points) + 'HPs left to live')
        add_pokemon = input("Do you want to add " + enemy_name + " to your collection? (answer 'yes' or 'no')")
        if add_pokemon == 'yes':
            pokedex[enemy_name] = enemy_pokemon
            pokedex_view()
            keep_playing()
        else:
            first_goer()
            battle()
    elif enemy_move_power > user_move_power:
        winner = 'Enemy'
        print(enemy_name + ' wins. You have been defeated!')
        update_hps()
        end_game()
        enemy_take_decision()
        keep_playing()
    else:
        winner = None
        print('No clear winner here. Just two frustrated pokemon!')
        first_goer()
        battle()


def keep_playing():
    switch_pokemon()
    first_goer()
    battle()


# winner of previous battle gets to go first
# randomly selects either enemy or user to go first where no clear winner in previous battle
def first_goer():
    if winner == 'User':
        get_move()
        enemy_choice()
    elif winner == 'Enemy':
        enemy_choice()
        get_move()
    else:
        first_battle_move = random.randint(1, 2)
        if first_battle_move == 1:
            get_move()
            enemy_choice()
        else:
            enemy_choice()
            get_move()

            
# asks user if they want to check pokedex then returns keys (names of pokemons) within pokedex dictionary
def pokedex_view():
    while True:
        pokedex_view_input = input("Do you want to check your pokedex? (answer 'yes' or 'no')")
        if pokedex_view_input == 'yes':
            print(list(pokedex.keys()))
            break
        elif pokedex_view_input == 'no':
            break
        else:
            print("Please only answer 'yes' or 'no'")

            
# asks user if they want to switch their current pokemon or keep current one
def switch_pokemon():
    while True:
        if len(pokedex) > 1:
            switch_pokemon_input = input("Would you like to switch your pokemon? (answer 'yes' or 'no').")
            if switch_pokemon_input == 'yes':
                next_pokemon_info()
                break
            elif switch_pokemon_input == 'no':
                break
            else:
                print("Please only answer 'yes' or 'no'")


# when enemy wins, an equivalent amount to the power difference between moves is deducted from the total HPs               
def update_hps():
    if winner == 'Enemy':
        lost_health_points = (enemy_move_power if user_move_power == 0 else enemy_move_power - user_move_power)
        global health_points
        health_points = health_points - lost_health_points
        print('Your HPs balance is: ' + str(health_points))

# if enemy wins, they might decide (randomly) to keep your pokemon
def lose_pokemon():
    global enemy_takes
    global next_pokemon
    enemy_takes = random.randint(1, 2)
    if enemy_takes == 1:
        try:
            pokedex.pop(next_pokemon['name'])
            print('Your enemy is stealing ' + next_pokemon['name'] + '. Please select a new pokemon from your pokedex.')
        except NameError:
            pokedex.pop(pokemon_name)
            print('Your enemy is keeping ' + pokemon_name + '. Please select a new pokemon from your pokedex.')
        pokedex_view()
    else:
        print('Your enemy has decided to let you keep your current pokemon')
        pokedex_view()


# If you only have one pokemon left, the enemy will let you keep it
def enemy_take_decision():
    global enemy_takes
    if len(pokedex) > 1:
        lose_pokemon()
        next_pokemon_info()
        first_goer()
        battle()
    elif len(pokedex) == 1:
        print('Lucky! Your enemy has decided to let you keep your lone warrior')
        first_goer()
        battle()


# this function allows the user, once they reach 0 HPs, to go back to 250 HPs and continue game, by losing a random pokemon from their pokedex. 
#If only one pokemon was left, the game ends.
def end_game():
    global health_points
    if health_points <= 0 and len(pokedex) > 1:
        exit_input = input("Your HPs are zero. Do you want to swap a random card from your "
                           "pokedex to go back to 250 HPs? (answer 'yes' or 'no')")
        if exit_input == 'yes':
            random_remove = random.choice(list(pokedex))
            pokedex.pop(random_remove)
            health_points = 250
            pokedex_view()
            next_pokemon_info()
            first_goer()
            battle()
        elif exit_input == 'no':
            print('Looks like you need to take a break from this game and try again later. \n')
            save_record()
            exit(keep_playing())
        else:
            print("Please only answer 'yes or 'no'.")
    elif health_points <= 0 and len(pokedex) == 1:
        print('Looks like you need to take a break from this game and try again later. \n')
        save_record()
        exit(keep_playing())


date_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# This saves pokedex record at the time the game ends
def save_record():
    # Creates new file if not already there
    games_record = open('games_record.txt', 'a')
    # Append contents of pokedex and date at the end of file
    print('Your pokedex record has been saved.')
    games_record.write('Your pokedex record shows: ' + str(list(pokedex.keys())) + ' on ' + date_time + '\n')
    # Close the file
    games_record.close()


begin_game()
get_move()
enemy_choice()
battle()
keep_playing()
