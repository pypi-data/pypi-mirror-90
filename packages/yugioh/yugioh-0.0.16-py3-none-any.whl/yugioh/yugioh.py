import requests

base_url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'

class card:
    def __init__(self, card_name):
        parameters = {'name':str(card_name)}
        card = requests.get(base_url, params=parameters).json()
        self.desc = card['data'][0]['desc']
        self.id = card['data'][0]['id']
        self.name = card['data'][0]['name']
        self.race = card['data'][0]['race']
        self.type = card['data'][0]['type']
        self.cardmarket_price = card['data'][0]['card_prices'][0]['cardmarket_price']
        self.tcgplayer_price = card['data'][0]['card_prices'][0]['tcgplayer_price']
        self.ebay_price = card['data'][0]['card_prices'][0]['ebay_price']
        self.amazon_price = card['data'][0]['card_prices'][0]['amazon_price']
        self.coolstuffinc_price = card['data'][0]['card_prices'][0]['coolstuffinc_price']
        if 'monster' in str(card['data'][0]['type']).lower():
            self.name = card['data'][0]['name']
            self.atk = card['data'][0]['atk']
            self.attribute = card['data'][0]['attribute']
            self._def = card['data'][0]['def']
            self.desc = card['data'][0]['desc']
            self.id = card['data'][0]['id']
            self.level = card['data'][0]['level']
            self.race = card['data'][0]['race']
            self.type = card['data'][0]['type']
            self.cardmarket_price = card['data'][0]['card_prices'][0]['cardmarket_price']
            self.tcgplayer_price = card['data'][0]['card_prices'][0]['tcgplayer_price']
            self.ebay_price = card['data'][0]['card_prices'][0]['ebay_price']
            self.amazon_price = card['data'][0]['card_prices'][0]['amazon_price']
            self.coolstuffinc_price = card['data'][0]['card_prices'][0]['coolstuffinc_price']
            if 'archetype' in card:
                self.archetype = card['data'][0]['archetype']

class get_card_by_id:
    def __init__(self, card_id):
        parameters = {'id':str(card_id)}
        card = requests.get(base_url, params=parameters).json()
        self.desc = card['data'][0]['desc']
        self.id = card['data'][0]['id']
        self.name = card['data'][0]['name']
        self.race = card['data'][0]['race']
        self.type = card['data'][0]['type']
        self.cardmarket_price = card['data'][0]['card_prices'][0]['cardmarket_price']
        self.tcgplayer_price = card['data'][0]['card_prices'][0]['tcgplayer_price']
        self.ebay_price = card['data'][0]['card_prices'][0]['ebay_price']
        self.amazon_price = card['data'][0]['card_prices'][0]['amazon_price']
        self.coolstuffinc_price = card['data'][0]['card_prices'][0]['coolstuffinc_price']
        if 'monster' in str(card['data'][0]['type']).lower():
            self.atk = card['data'][0]['atk']
            self.attribute = card['data'][0]['attribute']
            self._def = card['data'][0]['def']
            self.level = card['data'][0]['level']
            self.type = card['data'][0]['type']
            self.cardmarket_price = card['data'][0]['card_prices'][0]['cardmarket_price']
            self.tcgplayer_price = card['data'][0]['card_prices'][0]['tcgplayer_price']
            self.ebay_price = card['data'][0]['card_prices'][0]['ebay_price']
            self.amazon_price = card['data'][0]['card_prices'][0]['amazon_price']
            self.coolstuffinc_price = card['data'][0]['card_prices'][0]['coolstuffinc_price']
            if 'archetype' in card:
                self.archetype = card['data'][0]['archetype']

class get_cards_by_name:
    def __init__(self, keyword):
        parameters = {'fname':str(keyword)}
        cards = requests.get(base_url, params=parameters).json()
        self.list_of_cards = [card['name'] for card in cards['data']]
