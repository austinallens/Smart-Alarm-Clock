import random

print("ok")
Flashcards = {
    "Capital of France": "Paris",
    "Element with the lowest atomic weight": "Hydrogen",
    "How often should you tune a piano":"once a year"
}

def createCards (question,answer):
    Flashcards[question]=answer
    return dictionary


def askQuestion ():
    print ("ok")
    question = random.choice(list(Flashcards.keys()))
    answer = input(f"What is the answer for '{question}'?")

    correct_value = Flashcards[question]

    if answer == correct_value:
        print("correct")
    else:
        print("Try again!")

poiu = askQuestion()