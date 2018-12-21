# Gets list of questions from DB
def get_questions(c, table_name='questions'):
    c.execute('SELECT "question" FROM {tn}'.
              format(tn=table_name))
    question_list = c.fetchall()
    return question_list


# Gets question from input of character
def get_question_from_char(c, ch, table_name='questions'):
    c.execute('SELECT question FROM {tn} WHERE char = "{ch}"'.
              format(tn=table_name, ch=ch))
    question = c.fetchall()
    return question


# Gets list of animals from DB
def get_animals(c, table_name='animal_test'):
    c.execute('SELECT "animal" FROM {tn}'.
              format(tn=table_name))
    animals = c.fetchall()
    return animals


# Gets list of characters from DB
def get_chars(c, table_name='animal_test'):
    c.execute('PRAGMA table_info({tn})'
              .format(tn=table_name))
    columns = c.fetchall()
    chars = [x[1] for x in columns]
    chars = chars[1:]
    chars.sort()
    return chars


# From input char, returns list of t/f values of whether or not an animal has the characteristic
def get_animals_with_char(c, char, table_name='animal_test'):
    c.execute('SELECT {c} FROM {tn}'.format(c=char, tn=table_name))
    animals_with_char = c.fetchall()
    return animals_with_char


# from input animal, returns list of t/f values of whether or not characteristic belongs to animal
def get_chars_of_animal(c, animal, table_name='animal_test'):
    c.execute('SELECT * from {tn} where animal="{a}"'.format(tn=table_name, a=animal))
    chars_of_animals = c.fetchall()
    return chars_of_animals[0]


# Adds row to DB
def add_row_to_db(c, animal, chars, table_name='animal_test'):
    #for char in chars:
    #    char = char.to
    #print("chars: {}".format(chars))
    chars = '", "'.join(str(char) for char in chars)
    chars = '"' + chars + '"'
    #print(chars)
    c.execute('INSERT INTO "{tn}" VALUES ("{a}", {chars})'\
              .format(tn=table_name, a=animal, chars=chars))

