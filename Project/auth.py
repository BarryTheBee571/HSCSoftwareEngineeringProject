import json
import os
import hashlib
import secrets

USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")


def build_empty_accuracy_bucket():
    return {
        "tests": 0,
        "correct": 0,
        "answered": 0,
        "accuracy_sum": 0.0,
        "average_accuracy": 0.0,
    }


def ensure_user_stats_shape(user):
    user.setdefault("high_score", 0)
    user.setdefault("games_played", 0)
    user.setdefault("total_correct", 0)
    user.setdefault("total_answered", 0)
    user.setdefault("tests_started", 0)
    user.setdefault("total_time_spent_seconds", 0)
    user.setdefault("longest_unlimited_streak", 0)

    mode_counts = user.setdefault("mode_counts", {})
    for mode in ["addition", "subtraction", "multiplication", "division", "mixed"]:
        mode_counts.setdefault(mode, 0)
    user.setdefault("most_played_game_mode", "none")

    difficulty_stats = user.setdefault("difficulty_stats", {})
    for difficulty in ["easy", "medium", "hard"]:
        difficulty_stats.setdefault(difficulty, build_empty_accuracy_bucket())

    time_mode_stats = user.setdefault("time_mode_stats", {})
    for time_mode in ["30", "60", "90", "120", "unlimited"]:
        time_mode_stats.setdefault(time_mode, build_empty_accuracy_bucket())

    game_mode_stats = user.setdefault("game_mode_stats", {})
    for mode in ["addition", "subtraction", "multiplication", "division", "mixed"]:
        game_mode_stats.setdefault(mode, build_empty_accuracy_bucket())


def get_time_mode_key(time_limit):
    if time_limit is None:
        return "unknown"
    if time_limit < 0:
        return "unlimited"
    return str(time_limit)


def update_accuracy_bucket(bucket, correct, total_answered):
    accuracy = (correct / total_answered * 100) if total_answered > 0 else 0.0
    bucket["tests"] += 1
    bucket["correct"] += correct
    bucket["answered"] += total_answered
    bucket["accuracy_sum"] += accuracy
    bucket["average_accuracy"] = (
        bucket["accuracy_sum"] / bucket["tests"] if bucket["tests"] > 0 else 0.0
    )


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        try:
            return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return {}


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register(username, password):
    if len(username.strip()) < 3:
        return False, "Username must be at least 3 characters"
    if len(password) < 4:
        return False, "Password must be at least 4 characters"
    if " " in username:
        return False, "Username can't have spaces"

    users = load_users()

    if username in users:
        return False, "Username already taken"

    token = secrets.token_hex(16)

    users[username] = {
        "password": hash_password(password),
        "token": token,
        "high_score": 0,
        "games_played": 0,
        "total_correct": 0,
        "total_answered": 0,
        "tests_started": 0,
        "total_time_spent_seconds": 0,
        "longest_unlimited_streak": 0,
        "mode_counts": {
            "addition": 0,
            "subtraction": 0,
            "multiplication": 0,
            "division": 0,
            "mixed": 0,
        },
        "most_played_game_mode": "none",
        "difficulty_stats": {
            "easy": build_empty_accuracy_bucket(),
            "medium": build_empty_accuracy_bucket(),
            "hard": build_empty_accuracy_bucket(),
        },
        "time_mode_stats": {
            "30": build_empty_accuracy_bucket(),
            "60": build_empty_accuracy_bucket(),
            "90": build_empty_accuracy_bucket(),
            "120": build_empty_accuracy_bucket(),
            "unlimited": build_empty_accuracy_bucket(),
        },
        "game_mode_stats": {
            "addition": build_empty_accuracy_bucket(),
            "subtraction": build_empty_accuracy_bucket(),
            "multiplication": build_empty_accuracy_bucket(),
            "division": build_empty_accuracy_bucket(),
            "mixed": build_empty_accuracy_bucket(),
        },
    }
    save_users(users)
    return True, token


def login(username, password):
    users = load_users()

    if username not in users:
        return False, "Username not found"

    if users[username]["password"] != hash_password(password):
        return False, "Incorrect password"

    token = secrets.token_hex(16)
    users[username]["token"] = token
    save_users(users)
    return True, token


def get_user(username):
    users = load_users()
    user = users.get(username)
    if not user:
        return None
    ensure_user_stats_shape(user)
    return user


def record_test_started(username, mode):
    users = load_users()
    if username not in users:
        return

    user = users[username]
    ensure_user_stats_shape(user)
    user["tests_started"] += 1

    if mode in user["mode_counts"]:
        user["mode_counts"][mode] += 1
        user["most_played_game_mode"] = max(
            user["mode_counts"],
            key=lambda m: user["mode_counts"][m],
        )

    save_users(users)


def update_stats(
    username,
    score,
    correct,
    total_answered,
    mode,
    difficulty,
    time_limit,
    time_spent_seconds,
    longest_streak_in_test,
):
    users = load_users()
    if username not in users:
        return

    user = users[username]
    ensure_user_stats_shape(user)
    user["games_played"] += 1
    user["total_correct"] += correct
    user["total_answered"] += total_answered
    user["total_time_spent_seconds"] += max(0, int(round(time_spent_seconds)))

    if difficulty in user["difficulty_stats"]:
        update_accuracy_bucket(user["difficulty_stats"][difficulty], correct, total_answered)

    time_mode = get_time_mode_key(time_limit)
    if time_mode in user["time_mode_stats"]:
        update_accuracy_bucket(user["time_mode_stats"][time_mode], correct, total_answered)
    if time_mode == "unlimited":
        user["longest_unlimited_streak"] = max(
            user["longest_unlimited_streak"],
            int(longest_streak_in_test),
        )

    if mode in user["game_mode_stats"]:
        update_accuracy_bucket(user["game_mode_stats"][mode], correct, total_answered)

    if score > user["high_score"]:
        user["high_score"] = score

    save_users(users)


def get_high_score(username):
    user = get_user(username)
    if user:
        return user["high_score"]
    return 0
