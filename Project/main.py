import random
import time


def generate_question(mode, difficulty):
    ranges = {"easy": (1, 10), "medium": (1, 20), "hard": (1, 50)}
    lo, hi = ranges[difficulty]
 
    if mode == "mixed":
        mode = random.choice(["addition", "subtraction", "multiplication", "division"])
 
    if mode == "addition":
        answer = random.randint(lo * 2, hi * 2)
        a      = random.randint(lo, answer - lo)
        b      = answer - a
        return f"{a} + {b}", answer
 
    elif mode == "subtraction":
        answer = random.randint(lo, hi)
        b      = random.randint(lo, hi)
        a      = answer + b
        return f"{a} - {b}", answer
 
    elif mode == "multiplication":
        answer  = random.randint(lo, hi)
        factors = [i for i in range(lo, min(hi, 12) + 1) if answer % i == 0]
        if factors:
            a = random.choice(factors)
            b = answer // a
        else:
            a      = random.randint(lo, min(hi, 12))
            b      = random.randint(lo, min(hi, 12))
            answer = a * b
        return f"{a} x {b}", answer
 
    elif mode == "division":
        answer = random.randint(lo, hi)
        b      = random.randint(max(1, lo), min(hi, 12))
        a      = answer * b
        return f"{a} / {b}", answer

def pick_option(prompt, options):
    print(prompt)
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        choice = input("Enter number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("Invalid choice, try again.")

def main():
    print("MATHS SPEED CHALLENGE")

    mode       = pick_option("\nSelect mode:", ["addition", "subtraction", "multiplication", "division", "mixed"])
    difficulty = pick_option("\nSelect difficulty:", ["easy", "medium", "hard"])
    time_limit = 30

    print(f"\nYou have {time_limit} seconds. Press ENTER after each answer.")
    input("Press ENTER to start...")

    score              = 0
    questions_answered = 0
    correct_answers    = 0
    start_time         = time.time()

    while True:
        elapsed = time.time() - start_time
        if elapsed >= time_limit:
            break

        question, answer = generate_question(mode, difficulty)
        remaining = int(time_limit - elapsed)
        print(f"\n[{remaining}s left | Score: {score}]  {question} = ", end="")

        try:
            user_input = input().strip()
        except EOFError:
            break

        if time.time() - start_time >= time_limit:
            break

        questions_answered += 1

        if not user_input.lstrip("-").isdigit():
            print("Invalid input — skipped.")
            continue

        if int(user_input) == answer:
            correct_answers += 1
            score           += 10
            print("Correct!")
        else:
            print(f"Wrong. Answer was {answer}.")

    accuracy = (correct_answers / questions_answered * 100) if questions_answered else 0
    print("ROUND OVER!")
    print(f"  Score:     {score} pts")
    print(f"  Answered:  {questions_answered}")
    print(f"  Correct:   {correct_answers}")
    print(f"  Accuracy:  {accuracy:.1f}%")

main()