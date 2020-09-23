import requests
from foods.models import Food

foods = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?action=process&page_size=1000&json=1').json()['products']

food_name_check = []

for food in foods:
    if 'product_name' in food and 'nutrition_grades' in food and 'url' in food and 'selected_images' in food and 'front' in food['selected_images'] and 'categories_hierarchy' in food and food['product_name'] not in food_name_check:
        a = 0
        while 'based-foods' in food['categories_hierarchy'][a][3:] or 'potatoes' in food['categories_hierarchy'][a][3:]:
            a += 1
        current_food = Food(
            name=food['product_name'],
            nutriscore=food['nutrition_grades'],
            url=food['url'],
            image=food['selected_images']['front']['display']['fr'],
            category=food['categories_hierarchy'][a][3:]
        )
        food_name_check.append(food['product_name'])
        current_food.save()
