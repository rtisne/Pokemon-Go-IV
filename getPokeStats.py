import argparse
from pgoapi import pgoapi
import os
import json
import pprint

def init_config():
    parser = argparse.ArgumentParser()
    config_file = "config.json"
    load = {}
    if os.path.isfile(config_file):
        with open(config_file) as data:
            load.update(json.load(data))
    load = load['accounts']
    if load['auth_service'] not in ['ptc', 'google']:
      log.error("Invalid Auth service specified! ('ptc' or 'google')")
      return None

    return load


pokemon_names = json.load(open("name_id.json"))


config = init_config()

pokeapi = pgoapi.PGoApi()
login_name = config['username']
password = config['password']
service = config['auth_service']
lat = config['lat']
long = config['long']

pokeapi.login(service, login_name, password, float(lat), float(long), 10)
request = pokeapi.create_request()
request.get_inventory()
response = request.call()

items = response['responses']['GET_INVENTORY']['inventory_delta']['inventory_items']

print "nickname,species,attack_IV,defense_IV,stamina_IV,percent,cp"
for item in items:
    if 'pokemon_data' in item['inventory_item_data']:
        # Eggs are treated as pokemon by Niantic.
         if 'is_egg' not in item['inventory_item_data']['pokemon_data']:
            pokedata = item['inventory_item_data']['pokemon_data']
            attack_IV = pokedata.get('individual_attack', 0)
            defense_IV = pokedata.get('individual_defense', 0)
            stamina_IV = pokedata.get('individual_stamina', 0)
            percent = float(attack_IV + defense_IV + stamina_IV)/45. * 100.
            percent = "%.2f" % percent
            cp = str(pokedata.get('cp', 0))
            species = pokemon_names[str(pokedata.get('pokemon_id', 0))]
            nickname = pokedata.get('nickname', 'no_nickname')
            print "%s,%s,%s,%s,%s,%s,%s" %(nickname, species.encode('utf-8'), str(attack_IV), str(defense_IV), str(stamina_IV), percent, cp)
