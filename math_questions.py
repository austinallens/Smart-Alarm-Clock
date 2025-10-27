
import random

class MathQuestionGenerator:
    """
    Generates simple random math questions with multiple difficulty levels
    """

    def __init__(self, difficulty="Easy"):
        self.difficulty = difficulty
        self.operations = ['+', '-', '*', '/']

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
                if abs(selected - correct_answer) < 0.001:
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

# Example usage
if __name__ == "__main__":
    generator = MathQuestionGenerator(difficulty="Medium")
    # Keep asking until the user gets it correct
    while not generator.ask_question():
        pass