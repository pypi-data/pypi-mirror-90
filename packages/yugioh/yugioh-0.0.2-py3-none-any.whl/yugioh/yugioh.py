import requests

base_url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'

class monster:
    def __init__(self, card_name):
        parameters = {'name':str(card_name)}
        card = requests.get(base_url, params=parameters).json()
        self.name = card['data'][0]['name']
        self.archetype = card['data'][0]['archetype']
        self.atk = card['data'][0]['atk']
        self.attribute = card['data'][0]['attribute']
        self._def = card['data'][0]['def']
        self.desc = card['data'][0]['desc']
        self.id = card['data'][0]['id']
        self.level = card['data'][0]['level']
        self.race = card['data'][0]['race']
        self.type = card['data'][0]['type']

class spell:
    def __init__(self, card_name):
        parameters = {'name':str(card_name)}
        card = requests.get(base_url, params=parameters).json()
        self.desc = card['data'][0]['desc']
        self.id = card['data'][0]['id']
        self.name = card['data'][0]['name']
        self.race = card['data'][0]['race']
        self.type = card['data'][0]['type']
        
class trap:
    def __init__(self, card_name):
        parameters = {'name':str(card_name)}
        card = requests.get(base_url, params=parameters).json()
        self.desc = card['data'][0]['desc']
        self.id = card['data'][0]['id']
        self.name = card['data'][0]['name']
        self.race = card['data'][0]['race']
        self.type = card['data'][0]['type']
