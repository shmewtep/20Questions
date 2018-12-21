# CPTR460 software engineering
# Kelsey Rook
# Animal 20 Questions project

import sqlite3
import time
import db_manip as dm
import Game

def main():
    # open connection to DB
    sqlite_file = './db/db.db'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    # table_name = 'animal_test'
    # chars = ['can_keep_as_pet', 'has_fur', 'has_four_legs', 'is_carnivore', 'lives_in_water']
    chars = dm.get_chars(c)
    animals = dm.get_animals(c)

    game = Game.Game(chars, animals, c)

    print("Welcome to 20 Questions!")
    print("Please think of an animal...")
    time.sleep(.25)
    print('...')
    time.sleep(.25)
    print('...')
    time.sleep(.25)
    print('...')
    input("Press Enter when you've thought of an animal.")
    print("Awesome! I'll bet it's super easy to guess... \n")
    print("Here's my first question for you.")

    for i in range(0, 20):
        game.ask_next_question()

    correct = game.guess_winner()
    if correct:
        print("I told you I could guess it!")
    else:
        print("Ahem... I was just distracted. I'll bet I can get it now!")
        correct = game.guess_winner()
        if correct:
            print("Ha! Told you so! I'm smarter than you thought :)")
        else:
            print("Heh... you got me this time.")
            newAnimal = input("Can you tell me what animal you were thinking of so that I can remember it later?")
            print("I'm gonna ask you a few more questions.")
            for i in range(0, 4):
                game.ask_next_question()
            if newAnimal not in game.animals:
                dm.add_row_to_db(c, newAnimal, game.newAnimal)

    # commit changes to and close DB
    conn.commit()
    conn.close()

main()
