import random

Flashcards = {

}

def createCards (question,answer):
    Flashcards[question]=answer
    return dictionary


def askQuestion ():
    question = random.choice(list(Flashcards.keys()))
    answer = input(f"What is the answer for '{question}'?")

    correct_value = Flashcards[question]

    if answer == correct_value:
        print("correct")
    else:
        print("Try again!")
