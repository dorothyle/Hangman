'''
Class WordGuesser will select a random word from a given list, replace
the blanks if necessary, account for guesses and errors made, and
determine if the game is won or not.
'''

import random


class WordGuesser:
    def __init__(self, word_list):
        # Selects a random word
        self.answer = random.choice(word_list)

        # Creates string of blank lines
        self.dashes = ''.join(['_' for letter in self.answer])

        # Initializes errors made by user to 0
        self.errors = 0

        # Stores guessed letters in list
        self.guesses = []

    # Returns whether the guessed letter is in the word
    def is_correct_guess(self, guess):
        if guess not in self.answer:
            self.guesses.append(guess.upper())
        return guess in self.answer

    # Updates blank lines to show guessed letter
    def update_blanks(self, guess):
        index = []
        i = 0
        while i < len(self.answer):
            if guess in self.answer[i:]:
                index.append(self.answer[i:].index(guess) + i)
                i = self.answer[i:].index(guess) + i
            else:
                break
            i += 1
        for i in index:
            self.dashes = self.dashes[:i] + guess + self.dashes[i + 1:]

    # Increments the number of errors made by the user
    def increment_errors(self):
        self.errors += 1

    # Shows the hangman diagram based on the number of errors made
    # def show_diagram(self):
    #     print(HANGMAN[self.errors])

    def won(self):
        return '_' not in self.dashes

    def lost(self):
        return self.errors == 6

    # Determines whether game is over
    def game_over(self):
        return self.won() or self.lost()

    # Check if the user has already guessed the letter and prompt for another one
    def already_guessed(self, guess):
        return guess.upper() in self.guesses
