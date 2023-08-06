# yugioh

**YGOPRODECK API Wrapper**

## Installation

You can install it with pip3:

    pip3 install yugioh

## Usage

I'm currently still building this project. Monster cards are supported, spell/trap cards are not.

```python3
    from yugioh import yugioh
    
    card = yugioh(card_name = "The Wicked Dreadroot")
    print(card.name) #Returns "The Wicked Dreadroot"
    print(card.archetype) #Returns "Wicked God"
    print(card.atk) #Returns "4000"
```

# Attributes

Attribute | Description
------------ | -------------
name | The card's name
archetype | The card's archetype
atk | The card's attack points
attribute | The card's attribute
_def | The card's defense points
desc | The card's description
id | The card's ID
level | The card's level
race | The card's "race" (Still thinking about this one - Its documented in the API as "race", but is formally called "type")
type | Monster/Normal card
