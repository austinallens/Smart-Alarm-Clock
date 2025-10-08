
import random

class MathQuestionGenerator:
    """
    Generates simple random math questions (easy level)
    and checks user's answer.
    """

    def __init__(self):
        self.operations = ['+', '-', '*', '/']

    def generate_question(self):
        """Generate a random easy math question and answer."""
        op = random.choice(self.operations)

        # Random numbers for easy math
        a = random.randint(0, 10)
        b = random.randint(1, 10) if op == '/' else random.randint(0, 10)

        # Make division exact to avoid fractions
        if op == '/':
            a = a * b  # ensures a is divisible by b

        question = f"{a} {op} {b}"
        answer = self.calculate_answer(a, b, op)
        return question, answer

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
        question, correct_answer = self.generate_question()
        print("Solve this to turn off the alarm!")
        print("Question:", question)

        user_answer = input("Your answer: ")
        try:
            if int(user_answer) == correct_answer:
                print("Correct! Alarm off.")
                return True
            else:
                print(f"Wrong! The correct answer was {correct_answer}. Try again.")
                return False
        except ValueError:
            print("Please enter a number.")
            return False

# Example usage
if __name__ == "__main__":
    generator = MathQuestionGenerator()
    # Keep asking until the user gets it correct
    while not generator.ask_question():
        pass