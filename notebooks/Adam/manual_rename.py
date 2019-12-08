import pandas as pd
from tqdm import tqdm

def rename(df):
    for i, ingredient in enumerate(tqdm(df['ingredients_preformatted'])):
        for j, row_ingredient in enumerate(ingredient):
            if 'oil' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'oil'
                
            if 'pork' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'pork'
                
            if 'broth' in row_ingredient or 'stock' in row_ingredient or 'bouillon' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'broth'
                
            if 'chicken' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'chicken'
                
            if 'tomato' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'tomato'
                
            if 'beef' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'beef'

            if 'pepper' in row_ingredient and 'bell pepper' not in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'pepper'
            
            if 'salt' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'salt'
                
            if 'thyme' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'thyme'
                
            if 'lemon' in row_ingredient and 'lemongras' not in row_ingredient and 'lemon gras' not in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'lemon'
            
            if 'lime' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'lime'
            
            if 'vinegar' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'vinegar'
                
            if 'dijon mustard' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'mustard'
                
            if 'parsley' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'parsley'
                    
            if 'egg yolk' in row_ingredient or 'egg white' in row_ingredient or 'quail egg' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'egg'
                
            if 'ice cream' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'ice cream'      
                
            if 'cream' in row_ingredient and 'ice cream' not in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'cream'
                
            if 'cheese' in row_ingredient or 'mozzarella' in row_ingredient or 'feta' in row_ingredient or 'gruyere' in row_ingredient or 'gorgonzola' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'cheese'
                
            if 'mushroom' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'mushroom'  
                
            if 'sugar' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'sugar'  
                
            if 'mint' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'mint'  
                    
            if 'basil' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'basil'
                
            if 'fennel' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'fennel' 
                
            if 'ice cube' == row_ingredient:
                df['ingredients_preformatted'][i][j] = 'ice' 
                
            if 'cilantro' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'cilantro' 
                
            if 'chili' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'chili'    
                    
            if 'cumin' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'cumin' 
                
            if 'coriander' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'coriander' 
                
            if 'ice water' == row_ingredient or 'warm water' == row_ingredient:
                df['ingredients_preformatted'][i][j] = 'water' 
                
            if 'anchovy' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'anchovy' 
                
            if 'chocolate' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'chocolate' 

            if 'milk' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'milk' 
                
            if 'tarragon' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'tarragon'
                
            if 'liqueur' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'liqueur'
                
            if 'flour' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'flour'
                
            if 'onion' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'onion'
                
            if 'garlic' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'garlic'
                
            if 'gingerroot' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'ginger'
                
            if 'wine' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'wine'
                
            if 'potato' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'potato'

            if 'rosemary' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'rosemary'

            if 'tortilla' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'tortilla'

            if 'coconut' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'coconut'

            if 'lamb' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'lamb'

            if 'turkey' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'turkey'

            if 'broccoli' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'broccoli'

            if 'vanilla' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'vanilla'

            if 'orange peel' in row_ingredient or 'orange zest' in row_ingredient or 'orange juice' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'orange'

            if 'passion fruit juice' == row_ingredient:
                df['ingredients_preformatted'][i][j] = 'passion fruit'

            if 'apple juice' == row_ingredient or 'pippin apple' in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'vanilla'

            if 'juice' in row_ingredient:
                df['ingredients_preformatted'][i][j] = row_ingredient.split()[0]

            if 'rice' in row_ingredient and 'noodle' not in row_ingredient and 'licorice' not in row_ingredient:
                df['ingredients_preformatted'][i][j] = 'rice'

    return df