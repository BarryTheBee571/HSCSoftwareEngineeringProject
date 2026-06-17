import json
import os
import hashlib
import secrets

USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")


def _load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        try:
            return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return {}


def _save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def _hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register(username, password):
    if len(username.strip()) < 3:
        return False, "Username must be at least 3 characters"
    if len(password) < 4:
        return False, "Password must be at least 4 characters"
    if " " in username:
        return False, "Username can't have spaces"

    users = _load_users()

    if username in users:
        return False, "Username already taken"

    token = secrets.token_hex(16)

    users[username] = {
        "password":       _hash_password(password),
        "token":          token,
        "high_score":     0,
        "games_played":   0,
        "total_correct":  0,
        "total_answered": 0,
    }
    _save_users(users)
    return True, token


def login(username, password):
    users = _load_users()

    if username not in users:
        return False, "Username not found"

    if users[username]["password"] != _hash_password(password):
        return False, "Incorrect password"

    token = secrets.token_hex(16)
    users[username]["token"] = token
    _save_users(users)
    return True, token


def get_user(username):
    users = _load_users()
    return users.get(username)


def update_stats(username, score, correct, total_answered):
    users = _load_users()
    if username not in users:
        return

    user = users[username]
    user["games_played"]   += 1
    user["total_correct"]  += correct
    user["total_answered"] += total_answered

    if score > user["high_score"]:
        user["high_score"] = score

    _save_users(users)


def get_high_score(username):
    user = get_user(username)
    if user:
        return user["high_score"]
    return 0