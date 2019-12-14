import json

data = {}
data['Records'] = []

ingredients = ["chicken raw whole", "one bottle of wine png", "tomato", "milk carton", "ocet", "vanilla bean", "horcice" , "bell pepper", "soy sauce", "honey jar", "champignon", "celery root","celery", "chocolate bar", "scallion",
"majoneza", "almond", "chive", "bily jogurt"]
dir_names = ["chicken","wine","tomato","milk","vinegar","vanilla","horcice","bell pepper","soy sauce","honey", "mushroom","celery root","celery","chocolate","scallion","mayonnaise","almond","chive","yogurt"]

for (ingredient, dir_name) in zip(ingredients,dir_names):
    data['Records'].append({
        "keywords": ingredient,
        "limit": 60,
        "format": "jpg", 
        #"aspect_ratio": "square", #optional to get same image ratio
        "prefix": ingredient,
        "image_directory": dir_name
    })

with open('config.json', 'w') as outfile:
    json.dump(data, outfile)
