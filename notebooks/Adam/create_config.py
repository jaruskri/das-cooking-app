import json

data = {}
data['Records'] = []

ingredients = ["apple fruit", "grapes", "cucumber", "milk", "seafood", "mustard", "salt", "strawberry"]

for ingredient in ingredients:
    data['Records'].append({
        "keywords": ingredient,
        "limit": 5,
        "format": "png", 
        #"aspect_ratio": "square", #optional to get same image ratio
        "prefix": ingredient
    })

with open('config.json', 'w') as outfile:
    json.dump(data, outfile)