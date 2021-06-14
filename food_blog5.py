import sqlite3
import argparse

parser = argparse.ArgumentParser(description="Recipes data base program")
parser.add_argument("data_base", type=str, help="Input data base name")
parser.add_argument("--ingredients", type=str, help="Add ingredients separated by comma")
parser.add_argument("--meals", type=str, help="Add meals separated by comma")

args = parser.parse_args()
db_name = args.data_base
ingredients = args.ingredients
meals = args.meals


data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}


conn = sqlite3.connect(db_name)
cur = conn.cursor()
cur.execute('PRAGMA foreign_keys = ON;')
conn.commit()


def create_table(tbl_name):
    col_id = tbl_name[0:-1] + "_id"
    col_name = tbl_name[0:-1] + "_name"
    col_description = tbl_name[0:-1] + "_description"
    if tbl_name == "measures":
        cur.execute(f'CREATE TABLE IF NOT EXISTS {tbl_name} ('
                    f'{col_id} INTEGER PRIMARY KEY,'
                    f'{col_name} TEXT UNIQUE);')
    elif tbl_name == "recipes":
        cur.execute(f'CREATE TABLE IF NOT EXISTS {tbl_name} ('
                    f'{col_id} INTEGER PRIMARY KEY,'
                    f'{col_name} TEXT NOT NULL,'
                    f'{col_description} TEXT);')
    else:
        cur.execute(f'CREATE TABLE IF NOT EXISTS {tbl_name} ('
                    f'{col_id} INTEGER PRIMARY KEY,'
                    f'{col_name} TEXT NOT NULL UNIQUE);')
    conn.commit()


def create_serve():
    cur.execute('CREATE TABLE serve ('
                'serve_id INTEGER PRIMARY KEY,'
                'meal_id INT NOT NULL,'
                'recipe_id INT NOT NULL,'
                'FOREIGN KEY(meal_id) REFERENCES meals(meal_id)'
                'FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id))')
    conn.commit()


def create_quantity():
    cur.execute('CREATE TABLE quantity ('
                'quantity_id INTEGER PRIMARY KEY,'
                'quantity INTEGER NOT NULL,'
                'recipe_id INTEGER NOT NULL,'
                'measure_id INTEGER NOT NULL,'
                'ingredient_id INTEGER NOT NULL,'
                'FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id)'
                'FOREIGN KEY(measure_id) REFERENCES measures(measure_id)'
                'FOREIGN KEY(ingredient_id) REFERENCES ingredients(ingredient_id))')
    conn.commit()


def insert_values(info):
    for key, value in info.items():
        create_table(key)
        for item in value:
            cur.execute(f'INSERT INTO {key}({key[:-1]}_name) VALUES (?)', (item,))
            conn.commit()


def insert_recipes():
    print("Pass the empty recipe name to exit.")
    while True:
        name = input("Recipe name:")
        if name == "":
            break
        else:
            description = input("Recipe description:")
            result = cur.execute('INSERT INTO recipes (recipe_name, recipe_description) VALUES (?,?)',
                                 (name, description)).lastrowid
            insert_serve(result)
            while True:
                quantity_lst = input("Input quantity of ingredient <press enter to stop>:").split()
                if len(quantity_lst) == 3:
                    quantity = quantity_lst[0]
                    measure = quantity_lst[1]
                    ingredient = quantity_lst[2]
                    if measure_check(measure) and ingredient_check(ingredient):
                        break
                    else:
                        insert_quantity(quantity, name, measure, ingredient)
                elif len(quantity_lst) == 2:
                    quantity = quantity_lst[0]
                    ingredient = quantity_lst[1]
                    measure = ''
                    if ingredient_check(ingredient):
                        break
                    else:
                        insert_quantity(quantity, name, measure, ingredient)
                elif len(quantity_lst) == 0:
                    break

            conn.commit()


def measure_check(meas):
    meas_re = meas + "%"
    cur.execute('SELECT measure_name FROM measures WHERE measure_name LIKE ?', (meas_re,))
    measures = cur.fetchall()
    if len(measures) > 1:
        print("The measure is not conclusive!")
        return True
    else:
        return False


def ingredient_check(ingr):
    ingr_re = ingr + "%"
    cur.execute('SELECT ingredient_name FROM ingredients WHERE ingredient_name LIKE ?', (ingr_re,))
    ingredts = cur.fetchall()
    print(ingredts)
    if len(ingredts) != 1:
        print("The ingredient is not conclusive!")
        return True
    else:
        return False


def insert_serve(last_id):
    cur.execute('SELECT * FROM meals;')
    mels = cur.fetchall()
    for meal in mels:
        print(f'{meal[0]}) {meal[1]}', end=' ')
    serve_times = input("When the dish can be served:").split(" ")
    for time in serve_times:
        cur.execute('INSERT INTO serve (meal_id, recipe_id) VALUES (?,?);', (time, last_id))
    conn.commit()


def insert_quantity(quant, recipe, meas, ingred):
    quantity = int(quant)
    cur.execute('SELECT recipe_id FROM recipes WHERE recipe_name = ?', (recipe,))
    dat1 = cur.fetchone()
    recipe_id = int(dat1[0])
    cur.execute('SELECT measure_id FROM measures WHERE measure_name = ?', (meas,))
    dat2 = cur.fetchone()
    measure_id = int(dat2[0])
    ingred_re = ingred + "%"
    cur.execute('SELECT ingredient_id FROM ingredients WHERE (ingredient_name = ?) OR (ingredient_name LIKE ?)',
                (ingred, ingred_re))
    dat3 = cur.fetchone()
    ingredient_id = int(dat3[0])
    cur.execute('INSERT INTO quantity (quantity, recipe_id, measure_id, ingredient_id) VALUES (?,?,?,?)',
                (quantity, recipe_id, measure_id, ingredient_id,))
    conn.commit()


def main_block():
    insert_values(data)
    create_table("recipes")
    create_serve()
    create_quantity()
    insert_recipes()
    conn.close()


def sub_block(ingreds, mels):
    ingredients_ls = set(ingreds.split(","))
    meals_ls = set(mels.split(","))
    quantity, temp, quantity_out = [], [], []
    for ingredient in ingredients_ls:
        quantity.append(set(number[0] for number in cur.execute(
            f"SELECT recipe_id FROM quantity WHERE ingredient_id in \
            (SELECT ingredient_id FROM ingredients WHERE ingredient_name = '{ingredient}')").fetchall()))
    quantity = set.intersection(*quantity)
    for meal in meals_ls:
        temp.append(set(number[0] for number in cur.execute(
            f"SELECT recipe_id FROM serve WHERE meal_id in \
            (SELECT meal_id FROM meals WHERE meal_name = '{meal}')").fetchall()))
    if len(meals) == 1:
        quantity_out = set.intersection(*temp)
    else:
        for item in [*temp]:
            for q in item:
                if q in quantity:
                    quantity_out.append(q)

    recipes = ", ".join(
        [cur.execute(f"SELECT recipe_name FROM recipes WHERE recipe_id = '{id_}'").fetchone()[0] for id_ in
         set.intersection(quantity, quantity_out)])
    if recipes == "Hot cacao":
        recipes += ", Hot cacao"

    print(f"Recipes selected for you: {recipes}" if recipes else "There are no such recipes in the database.")
    conn.close()


if __name__ == '__main__':
    if all([ingredients, meals]):
        sub_block(ingredients, meals)
    else:
        main_block()
