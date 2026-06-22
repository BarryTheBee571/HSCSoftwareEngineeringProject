import random

def make_question(mode, difficulty):
    """Return one math question string + integer answer."""
    if difficulty not in ("easy", "medium", "hard"):
        raise ValueError(f"Invalid difficulty: {difficulty}")  # block unexpected difficulty values
    if mode == "mixed":
        mode = random.choice(["addition", "subtraction", "multiplication", "division"])  # randomize mode
    return make_by_mode(mode, difficulty)  # build question for chosen mode

def make_by_mode(mode, difficulty):
    """Route to the matching question builder."""
    if mode == "addition":
        return make_addition_q(difficulty)
    elif mode == "subtraction":
        return make_subtraction_q(difficulty)
    elif mode == "multiplication":
        return make_multiplication_q(difficulty)
    elif mode == "division":
        return make_division_q(difficulty)
    raise ValueError(f"Invalid mode: {mode}")  # fail fast on bad mode input

def make_addition_q(difficulty):
    """Generate addition where result stays in the selected range."""
    answer_ranges = {"easy": (1, 20), "medium": (1, 50), "hard": (1, 100)}  # target result ranges
    lo, hi = answer_ranges[difficulty]  # pick range from difficulty
    answer = random.randint(max(2, lo), hi)  # avoid too-small answers
    a = random.randint(1, answer - 1)  # first number
    b = answer - a  # second number gives exact answer
    return f"{a} + {b}", answer  # show text + true answer

def make_subtraction_q(difficulty):
    """Generate subtraction with no negative results."""
    operand_ranges = {"easy": (1, 20), "medium": (1, 50), "hard": (1, 100)}  # number ranges
    lo, hi = operand_ranges[difficulty]  # pick range by difficulty
    b = random.randint(lo, hi)  # subtractor
    a = random.randint(b, hi)  # make sure a >= b
    answer = a - b  # non-negative result
    return f"{a} - {b}", answer  # show text + true answer

def make_multiplication_q(difficulty):
    """Generate multiplication based on difficulty."""
    operand_ranges = {"easy": (1, 10), "medium": (1, 20), "hard": (1, 50)}  # number ranges
    lo, hi = operand_ranges[difficulty]  # pick range by difficulty
    a = random.randint(lo, hi)  # first factor
    b = random.randint(lo, hi)  # second factor
    answer = a * b  # multiply factors
    return f"{a} x {b}", answer  # show text + true answer

def make_division_q(difficulty):
    """Generate division that always has a whole-number answer."""
    answer_ranges = {"easy": (1, 10), "medium": (1, 20), "hard": (1, 50)}  # result ranges
    lo, hi = answer_ranges[difficulty]  # pick range by difficulty
    answer = random.randint(lo, hi)  # final integer answer
    b = random.randint(1, 12)  # divisor
    a = answer * b  # dividend chosen to divide cleanly
    return f"{a} ÷ {b}", answer  # show text + true answer