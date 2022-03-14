# from nltk.corpus import words
from colorama import init
from termcolor import *
import random
import string

MAX_GUESSES = 6
CUR_GUESSES = 0
WIN = False
ALPHABET = [0] * 26

class letter:
    def __init__(self, value: str, found: int):
        self.lett = value
        self.val = found
        return self
    
    def switch(self, found):
        self.val = found


answer_file = open("answer_words.txt", "r")
lines = answer_file.read()
answer_list = lines.splitlines()
answer_file.close()

guesses_file = open("valid_guesses.txt", "r")
line = guesses_file.read()
guesses_list = lines.splitlines()
guesses_file.close()

guesses_list += answer_list

colors = ['white', 'green', 'yellow', 'red']
# 0 = not entered yet
# 1 = right position
# 2 = in the word
# 3 = not in the word

def print_alphabet(alphabet):
    print("[", end=" ")

    for num, ind in enumerate(ALPHABET):
        print(colored(string.ascii_lowercase[num], colors[ind]), end = " ")

    print("]")

init()

# word_list = [word for word in words.words() if len(word) == 5]

answer_word = random.choice(answer_list)

print(f"You have {MAX_GUESSES} guesses to guess the 5 letter word.")
# print(answer_word)

while not WIN:  #core game loop
    guess = str(input("_ _ _ _ _"))
    if len(guess) != 5 or guess.lower() not in guesses_list:
        print("\033[A               \033[A")
        print(guess)
        continue

    CUR_GUESSES += 1
    print("\033[A               \033[A")

    winning = 0

    for ind, lett in enumerate(guess):
        guess_color = 0
        if lett in answer_word and ALPHABET[string.ascii_lowercase.index(lett)] != 1:
            ALPHABET[string.ascii_lowercase.index(lett)] = 2
            guess_color = 2

        if lett == answer_word[ind]:
            ALPHABET[string.ascii_lowercase.index(lett)] = 1
            guess_color = 1
            winning += 1

        if lett not in answer_word:
            ALPHABET[string.ascii_lowercase.index(lett)] = 3
            guess_color = 3

        print(colored(lett.upper(), colors[guess_color]), end=" ")
    
    print_alphabet(ALPHABET)
    
    if winning == 5:
        WIN = True
    elif CUR_GUESSES == 6:
        break

    
if WIN:
    print(f"\nYou got it in {CUR_GUESSES}/{MAX_GUESSES}.")
else:
    print(f"\nYou Lose! The word was {answer_word}.")