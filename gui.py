import sqlite3
import time
import db_manip as dm
import Game
from tkinter import *

# open connection to DB
sqlite_file = './db/db.db'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

chars = dm.get_chars(c)
animals = dm.get_animals(c)

game = Game.Game(chars, animals, c)

window = Tk()
window.title("20 Questions")
window.geometry('500x400')

lbl = Label(window, text="Welcome to 20Q!")
lbl.grid(column=0, row=0)
lbl = Label(window, text="Please think of an animal...")
lbl.grid(column=0, row=1)

#text = Text(window)
#text.insert(INSERT, 'Welcome to 20Q!\n')
#text.insert(INSERT, 'Please think of an animal...')
#text.pack()




window.mainloop()
