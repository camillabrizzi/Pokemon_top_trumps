import requests
import json
import random
from googletrans import Translator

random_user_pokemon = random.randint(1, 151)
url = 'https://pokeapi.co/api/v2/pokemon/{}'.format(random_user_pokemon)
response = requests.get(url).text
pokemon_info = json.loads(response)

# print name of specific pokemon in the list nested under 'results' key in response_info dictionary


first_pokemon = pokemon_info['name']
print('You have chosen ' + first_pokemon + '. Its moves are:  \n')

# print abilities for user's pokemon

for item in pokemon_info['moves']:
    print(item['move']['name'], end=', ')


# generates random pokemon and a random one of its moves for enemy
def enemy_choice():
    random_enemy_pokemon = random.randint(1, 151)
    url1 = 'https://pokeapi.co/api/v2/pokemon/{}'.format(random_enemy_pokemon)
    response1 = requests.get(url1).text
    enemy_info = json.loads(response1)
    enemy_name = enemy_info['name']
    print("Your enemy has chosen " + enemy_name + '\n')

    # generates random move from enemy's pokemon
    random_enemy_move = random.choice(enemy_info['moves'])
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


# function to ask user to choose move
def user_pokemon():
    print()
    user_choice = input('\nWhat move would you like to use? \n')
    print('You have chosen ' + user_choice + '\n')

    # retrieves info on user's move

    url2 = 'https://pokeapi.co/api/v2/move/{}'.format(user_choice)
    response2 = requests.get(url2).text
    move_info = json.loads(response2)
    move_comment = move_info['flavor_text_entries'][0]['flavor_text']
    translation = Translator()
    translated_comment = translation.translate(move_comment)
    print(translated_comment.text + '\n')


user_pokemon()
enemy_choice()
