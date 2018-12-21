import random
import db_manip as dm


class Game:
    def __init__(self, chars, animals, conn):
        self.question_number = 1
        self.chars = chars
        self.questions_asked = [0] * len(chars)
        self.animals_dict = {}
        self.animals = [i for i in range(0, len(animals))]
        for (animal_num, animal_name) in zip(self.animals, animals):
            self.animals_dict[animal_num] = animal_name
        self.questions = dm.get_questions(conn)
        self.c = conn
        self.points = []
        for i in range(len(animals)):
            self.points.append((i, 0))

        self.leng = len(chars)
        self.prevGuessed = " "
        self.newAnimal = [None] * len(chars)

    # Iterates through two arrays of characteristics; returns first characteristic that arrays DON'T have in common
    #   Checks that question corresponding to characteristic hasn't been asked
    def get_different_char(self, animal1_chars, animal2_chars, begin_num):

        for i in range(begin_num, len(self.chars)):
            if animal1_chars[i] != animal2_chars[i]:
                question_number = i
                print(question_number)

                # Checks that question has not already been asked; if it has, recursively calls function
                #       beginning with question after quest_number
                if self.questions_asked[question_number] == 1:
                    self.get_different_char(animal1_chars, animal2_chars, question_number + 1)
                else:
                    return question_number

        # If animals have no characters in common, return random question number
        new_rand_int = random.randint(0, self.leng) - 1

        # Makes sure that question hasn't already been asked
        while self.questions_asked[new_rand_int] == 1:
            new_rand_int = (new_rand_int + 1) % self.leng

            return new_rand_int

    # returns next question number
    def get_next_question(self):
        # For first 17 questions, return random question number
        if self.question_number <= 25:
            rand_int = random.randint(0, self.leng) - 1

            # Makes sure that question hasn't already been asked
            while self.questions_asked[rand_int] == 1:
                rand_int = (rand_int + 1) % self.leng


            return rand_int
        else:
            # get two animals with most points
            top2 = []
            points = self.points[:]
            highest = points[0]
            last_highest = highest
            for i in range(0, 2):
                for item in points:
                    if item[1] > highest[1]:
                        highest = (item[0], item[1])
                top2.append(highest[0])
                points.remove(highest)
                if last_highest == highest:
                    highest = points[0]
                last_highest = highest
                highest = points[0]

            animal1 = self.animals_dict[top2[0]]
            animal2 = self.animals_dict[top2[1]]

            # print(animal1[0])
            # print(animal2[0])

            animal1_chars_tuple = dm.get_chars_of_animal(self.c, animal1[0])
            animal2_chars_tuple = dm.get_chars_of_animal(self.c, animal2[0])

            # convert from tuple to array
            animal1_chars = []
            animal2_chars = []

            animal1_chars.append(animal1_chars_tuple)
            animal2_chars.append(animal2_chars_tuple)

            animal1_chars = [x for xs in animal1_chars for x in xs]
            animal2_chars = [x for xs in animal2_chars for x in xs]
            animal1_chars = animal1_chars[1:]
            animal2_chars = animal2_chars[1:]

            # get characteristic similar between two animals
            # increment question number
            question_num = self.get_different_char(animal1_chars, animal2_chars, 0)
            return question_num

    # asks question from those not already asked
    def ask_next_question(self):
        char_number = self.get_next_question()
        self.questions_asked[char_number] += 1
        char = self.chars[char_number]
        q = dm.get_question_from_char(self.c, char)

        # gets yes/no input from user
        ans = self.get_ans(q[0][0])

        self.newAnimal[char_number] = int(ans)
        animals_with_char = dm.get_animals_with_char(self.c, char)

        # increments question number
        self.question_number += 1

        # print("points: {}".format(self.points))
        for x in range(0, len(self.animals)):
            if ans == int(animals_with_char[x][0]):
                self.points[x] = (self.points[x][0], self.points[x][1] + 1)

    # gets yes/no answer from user; prompts again if answer is invalid
    def get_ans(self, q):
        ans = input('\n{} (y/n)'.format(q))
        if ans == 'y' or ans == 'Y' or ans == 'yes' or ans == 'Yes' or ans == 'YES':
            return 1
        if ans == 'n' or ans == 'N' or ans == 'No' or ans == 'no' or ans == 'NO':
            return 0
        else:
            print("You must enter a yes or no answer (i.e. y, n, yes, no, etc.")
            return self.get_ans(q)

    # returns animal with most points; asks user if correct or not
    def guess_winner(self):
        winner = (None, 0)
        for item in self.points:
            if winner[1] < item[1]:
                if item is not self.prevGuessed:
                    winner = item
        winner = self.animals_dict[winner[0]]
        q = ("\nWere you were thinking of a {}?".format(winner[0]))
        self.prevGuessed = winner
        correct = self.get_ans(q)
        return correct





