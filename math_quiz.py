import tkinter as tk
import random

def generate_question(difficulty):
    if difficulty == "Easy":
        a, b = random.randint(1, 10), random.randint(1, 10)
        op = random.choice(["+", "-"])
    elif difficulty == "Medium":
        a, b = random.randint(5, 20), random.randint(1, 12)
        op = random.choice(["+", "-", "*", "/"])

    question = f"{a} {op} {b}"
    try:
        correct_answer = round(eval(question), 2)
    except ZeroDivisionError:
        return generate_question(difficulty)

    # generate 3 wrong options
    options = [correct_answer]
    while len(options) < 4:
        wrong = round(correct_answer + random.uniform(-10, 10), 2)
        if wrong != correct_answer and wrong not in options:
            options.append(wrong)
    random.shuffle(options)

    return question, correct_answer, options


class MathQuestionFrame(tk.Frame):
    def __init__(self, parent, stop_alarm_callback, difficulty="Easy"):
        super().__init__(parent)
        self.stop_alarm_callback = stop_alarm_callback
        self.difficulty = difficulty
        self.correct_answer = None

        self.question_label = tk.Label(self, text="", font=("Arial", 16))
        self.question_label.pack(pady=10)

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(self, text="", width=15, font=("Arial", 12), command=lambda i=i: self.check_answer(i))
            btn.pack(pady=3)
            self.option_buttons.append(btn)

        self.status_label = tk.Label(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.new_question()

    def new_question(self):
        self.status_label.config(text="")
        question, answer, options = generate_question(self.difficulty)
        self.correct_answer = answer
        self.question_label.config(text=question)
        for i, btn in enumerate(self.option_buttons):
            btn.config(text=options[i])

    def check_answer(self, index):
        selected = float(self.option_buttons[index].cget("text"))
        if abs(selected - self.correct_answer) < 0.001:
            self.status_label.config(text="✅ Correct! Alarm stopped.", fg="green")
            self.stop_alarm_callback()
        else:
            self.status_label.config(text=f"❌ Wrong! Try again.", fg="red")
