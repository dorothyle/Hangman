from tkinter import *
import tkinter.messagebox as msgbox
from WordGuesser import WordGuesser

# Returns list of words in the file
def get_words(filename):
    infile = open(filename, 'r')
    lines = infile.read()
    words = lines.split('\n')
    return words

# Creates mode buttons and returns a list of the buttons
def create_mode_buttons():
    modes = ['EASY', 'MEDIUM', 'HARD']
    buttons = []
    for i in range(len(modes)):
        mode = modes[i]
        x = 0.25 + i * 0.25
        y = 0.60
        button = Button(window, text=mode, font=("Comic Sans MS", 16),
                        command=(lambda m=mode: select_mode(m)))
        button.place(relx=x, rely=y, relwidth=.2, relheight=.1, anchor='n')
        buttons.append(button)

    return buttons

# Determines the number of wrong guesses the player can have based
# on the selected difficulty and clears the screen
def select_mode(mode):
    for key, val in screen.items():
        if key != 'buttons':
            val.destroy()

        else:
            for button in val:
                button.destroy()

    screen.clear()

    if mode == 'EASY':
        num_guesses[0] = 10

    elif mode == 'MEDIUM':
        num_guesses[0] = 7

    elif mode == 'HARD':
        num_guesses[0] = 3

    setup_game()


# Creates the letter buttons and returns a list of buttons
def create_letter_buttons(root):
    buttons = []
    val = 65
    for row in range(3):
        y = 0.5 + row * 0.15
        if row == 2:
            col = 6
            begin = 0.24
        else:
            col = 10
            begin = 0.06
        for i in range(val, val + col):
            char = chr(i)
            x = begin + (i - val) * .09
            letter = Button(root, text=char, font=("Comic Sans MS", 25),
                            command=(lambda l=char: make_guess(l.lower())))
            letter.place(relx=x, rely=y, relwidth=0.06, relheight=0.12)
            buttons.append(letter)
        val += 10

    return buttons


# Displays length of the word, number of guesses left, letter the user has guessed,
# blank lines for the word, and buttons for guessing letters
def setup_game():
    screen['buttons'] = create_letter_buttons(window)
    game_progress = Frame(window)
    game_progress.place(relx=0.5, rely=0.3, relwidth=0.9, relheight=0.1, anchor='n')

    word_length_title = Label(game_progress, text='Length', font=("Comic Sans MS", 15))
    word_length_title.place(relx=0.05, rely=0.5, anchor='center')
    word_length = Label(game_progress, text=len(hangman_game.answer), font=("Comic Sans MS", 15),
                        borderwidth=3, relief='solid')
    word_length.place(relx=0.13, rely=0.5, relwidth=0.06, anchor='center')

    guesses_left_title = Label(game_progress, text="Guesses Left", font=("Comic Sans MS", 15))
    guesses_left_title.place(relx=0.27, rely=0.5, anchor='center')
    guesses_left = Label(game_progress, text=num_guesses, font=("Comic Sans MS", 15),
                         borderwidth=3, relief='solid')
    guesses_left.place(relx=0.395, rely=0.5, relwidth=0.06, anchor='center')

    wrong_guesses_title = Label(game_progress, text="Wrong Guesses", font=("Comic Sans MS", 15))
    wrong_guesses_title.place(relx=0.55, rely=0.5, anchor='center')
    wrong_guesses = Label(game_progress, text=', '.join(hangman_game.guesses), font=("Comic Sans MS", 15),
                          borderwidth=3, relief='solid')
    wrong_guesses.place(relx=0.82, rely=0.5, relwidth=0.34, anchor='center')
    blanks = Label(window, text=' '.join([char for char in hangman_game.dashes]), font=("Comic Sans MS", 30))
    blanks.place(relx=0.5, rely=0.15, anchor='center')

    screen['progress frame'] = game_progress
    screen['length'] = word_length
    screen['guesses left'] = guesses_left
    screen['wrong guesses'] = wrong_guesses
    screen['blanks'] = blanks


# Evaluates the guessed letter when user presses button
def make_guess(letter):
    if not hangman_game.game_over() or num_guesses != 0:
        # Check if guess has already been made and if the guess is correct
        eval_guess(letter)


# Updates GUI based on guess
def eval_guess(letter):
    # Updates blank lines with guessed letters if guesses correctly
    if hangman_game.is_correct_guess(letter):
        hangman_game.update_blanks(letter)
        screen['blanks'].configure(text=' '.join([char for char in hangman_game.dashes]))

    # Adds wrong letter to list of wrong guesses to be displayed and decrements number
    # of guesses the user has left
    else:
        screen['wrong guesses'].configure(text=', '.join(hangman_game.guesses))
        num_guesses[0] -= 1
        screen['guesses left'].configure(text=num_guesses)

    # Disabled buttons of guessed letters
    for button in screen['buttons']:
        if button['text'] == letter.upper():
            button.configure(state='disabled')

    # Outputs messages once game is over
    if hangman_game.won():
        msgbox.showinfo(title="Congratulations!", message="Congratulations! You won!")
        for button in screen['buttons']:
            button.configure(state='disabled')

    elif num_guesses[0] == 0:
        msgbox.showinfo(title="GAME OVER", message="Game over! You lost.\nThe word was '" + hangman_game.answer + "'.")
        for button in screen['buttons']:
            button.configure(state='disabled')


# Gets words from file
words = get_words("Words.txt")
hangman_game = WordGuesser(words)
num_guesses = [0]

# Creates window for user to enter letters
window = Tk()
window.title("Hangman")
window.configure(bg='light yellow')
window.geometry('700x400')

# Creates title
title = Label(window, text="Hangman", bg='light yellow', font=("Comic Sans MS", 40))
title.place(relx=0.5, rely=0.25, anchor='center')

# Prompts user to choose difficulty
instruction = Label( window, text="Please select a difficulty level.", bg='light yellow',
                    font=("Comic Sans MS", 20))
instruction.place(relx=0.5, rely=0.4, anchor='n')
mode_buttons = create_mode_buttons()

screen = {'title':title, 'instruction':instruction, 'buttons':mode_buttons}

window.mainloop()
