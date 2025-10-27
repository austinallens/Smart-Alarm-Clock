import random
from math_questions import MathQuestionGenerator

def generate_question(difficulty):
    """Generate a random math question and a few answer options."""
    if difficulty == "Easy":
        a, b = random.randint(1, 10), random.randint(1, 10)
        op = random.choice(["+", "-"])
    elif difficulty == "Medium":
        a, b = random.randint(5, 20), random.randint(1, 12)
        op = random.choice(["+", "-", "*"])
    else: # Default to Easy if unkown difficulty
        a, b = random.randint(1, 10), random.randint(1, 10)
        op = random.choice(["+", "-"])

    question = f"{a} {op} {b}"
    correct_answer = int(eval(question))

    # generate 3 wrong options
    options = [correct_answer]
    while len(options) < 4:
        wrong = correct_answer + random.randint(-10, 10)
        if wrong != correct_answer and wrong not in options:
            options.append(wrong)
    random.shuffle(options)

    return question, correct_answer, options

class MathQuestionGenerator:
    """
    Generates simple random math questions with multiple difficulty levels
    """

    def __init__(self, difficulty="Easy"):
        self.difficulty = difficulty
        self.operations = ['+', '-', '*', '/']

    def generate_question(self):
        """Generate a random math question and a few answer options."""
        # Use the standalone function to avoid code duplication
        return generate_question(self.difficulty)

    def set_difficulty(self, difficulty):
        """Update the difficulty level"""
        self.difficulty = difficulty

    @staticmethod
    def calculate_answer(a, b, op):
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            return a // b  # integer division
        else:
            return None

    def ask_question(self):
        """Ask the user the math question and check the answer."""
        question, correct_answer, options = self.generate_question()
        print("Solve this to turn off the alarm!")
        print("Question:", question)
        
        # Display multiple choice options
        print("\nChoose an answer:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        user_answer = input("Your answer (1-4): ")
        try:
            choice_index = int(user_answer) - 1
            if 0 <= choice_index < 4:
                selected = options[choice_index]
                if selected == correct_answer:
                    print("Correct! Alarm off.")
                    return True
                else:
                    print(f"Wrong! The correct answer was {correct_answer}. Try again.")
                    return False
            else:
                print("Please choose 1, 2, 3, or 4.")
                return False
        except ValueError:
            print("Please enter a number between 1 and 4.")
            return False


#class MathQuestionFrame(tk.Frame):
#    def __init__(self, parent, stop_alarm_callback, difficulty="Easy"):
#        super().__init__(parent)
#        self.stop_alarm_callback = stop_alarm_callback
#        self.difficulty = difficulty
#        self.correct_answer = None
#
#        self.generator = MathQuestionGenerator(difficulty=difficulty)
#
#        self.question_label = tk.Label(self, text="", font=("Arial", 16))
#        self.question_label.pack(pady=10)
#
#        self.option_buttons = []
#        for i in range(4):
#            btn = tk.Button(self, text="", width=15, font=("Arial", 12), command=lambda i=i: self.check_answer(i))
#            btn.pack(pady=3)
#            self.option_buttons.append(btn)
#
#        self.status_label = tk.Label(self, text="", font=("Arial", 12))
#        self.status_label.pack(pady=10)
#
#        self.new_question()
#
#    def new_question(self):
#        self.status_label.config(text="")
#        question, answer, options = self.generator.generate_question()
#        self.correct_answer = answer
#        self.question_label.config(text=question)
#        for i, btn in enumerate(self.option_buttons):
#            btn.config(text=options[i])
#
#    def check_answer(self, index):
#        selected = float(self.option_buttons[index].cget("text"))
#        if abs(selected - self.correct_answer) < 0.001:
#            self.status_label.config(text="✅ Correct! Alarm stopped.", fg="green")
#            self.stop_alarm_callback()
#        else:
#            self.status_label.config(text=f"❌ Wrong! Try again.", fg="red")

# Example usage
if __name__ == "__main__":
    print("Math Quiz Alarm!")
    difficulty = input("Choose difficulty (Easy/ Medium): ").strip().title()
    if difficulty not in ["Easy", "Medium"]:
        difficulty = "Easy"

    generator = MathQuestionGenerator(difficulty=difficulty)
    
    # Keep asking until the user gets it correct
    while not generator.ask_question():
        pass

    print("Alarm stopped!")