import random

def generate_question(mode, difficulty):
    if mode == "mixed":
        mode = random.choice(["addition", "subtraction", "multiplication", "division"])
        return _generate_by_mode(mode, difficulty)
    else:
        return _generate_by_mode(mode, difficulty)

def _generate_by_mode(mode, difficulty):
    if mode == "addition":
        return _generate_addition(difficulty)
    elif mode == "subtraction":
        return _generate_subtraction(difficulty)
    elif mode == "multiplication":
        return _generate_multiplication(difficulty)
    elif mode == "division":
        return _generate_division(difficulty)

def _generate_addition(difficulty):
    answer_ranges = {"easy": (1, 20), "medium": (1, 50), "hard": (1, 100)}
    lo, hi = answer_ranges[difficulty]
    answer = random.randint(max(2, lo), hi)
    a = random.randint(1, answer - 1)
    b = answer - a
    return f"{a} + {b}", answer

def _generate_subtraction(difficulty):
    operand_ranges = {"easy": (1, 20), "medium": (1, 50), "hard": (1, 100)}
    lo, hi = operand_ranges[difficulty]
    b = random.randint(lo, hi)
    a = random.randint(b, hi)
    answer = a - b
    return f"{a} - {b}", answer

def _generate_multiplication(difficulty):
    operand_ranges = {"easy": (1, 10), "medium": (1, 20), "hard": (1, 50)}
    lo, hi = operand_ranges[difficulty]
    a = random.randint(lo, hi)
    b = random.randint(lo, hi)
    answer = a * b
    return f"{a} x {b}", answer

def _generate_division(difficulty):
    answer_ranges = {"easy": (1, 10), "medium": (1, 20), "hard": (1, 50)}
    lo, hi = answer_ranges[difficulty]
    answer = random.randint(lo, hi)
    b = random.randint(1, 12)
    a = answer * b
    return f"{a} ÷ {b}", answer