import json
import os
import hashlib
import secrets

USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")  # local json db file

def make_blank_bucket():
    """Make a fresh stats bucket for one category."""
    return {
        "tests": 0,  # how many test runs
        "correct": 0,  # total correct answers
        "answered": 0,  # total attempted answers
        "average_accuracy": 0.0,  # running % score
    }

def pick_time_mode_key(time_limit):
    """Convert a time limit value into the matching stats key."""
    if time_limit < 0:  # -1 means no timer
        return "unlimited"  # special bucket key
    return str(time_limit)  # 30, 60, 90, 120

def add_to_bucket(bucket, correct, total_answered):
    """Update one stats bucket after a finished test."""
    bucket["tests"] += 1  # one more completed run
    bucket["correct"] += correct  # add correct count
    bucket["answered"] += total_answered  # add attempts count
    bucket["average_accuracy"] = (
        bucket["correct"] / bucket["answered"] * 100 if bucket["answered"] > 0 else 0.0  # safe divide
    )

def load_users():
    """Load users.json safely, or return empty data if file is bad/missing."""
    if not os.path.exists(USERS_FILE):  # first run case
        return {}  # no users yet
    with open(USERS_FILE, "r") as f:  # read file text
        try:
            return json.load(f)  # parse json into dict
        except (json.JSONDecodeError, ValueError):
            return {}  # fallback if file is broken

def save_users(users):
    """Write user data back to users.json."""
    with open(USERS_FILE, "w") as f:  # overwrite with latest data
        json.dump(users, f, indent=4)  # pretty print for readability

def scramble_password(password):
    """Hash a password before saving/checking it."""
    return hashlib.sha256(password.encode()).hexdigest()  # one-way hash

def register(username, password):
    """Create a new user account and return a session token."""
    if len(username.strip()) < 3:  # stop empty/super short names
        return False, "Username must be at least 3 characters"  # tell user why
    if len(password) < 4:  # basic password minimum
        return False, "Password must be at least 4 characters"  # show clear rule
    if " " in username:  # keep names simple
        return False, "Username can't have spaces"  # validation message

    users = load_users()  # load current accounts

    if username in users:  # prevent duplicates
        return False, "Username already taken"  # must be unique

    # token works like a quick session key
    token = secrets.token_hex(16)  # random session token

    users[username] = {
        "password": scramble_password(password),  # never store plain password
        "token": token,  # active session token
        "high_score": 0,  # personal best points
        "games_played": 0,  # finished games counter
        "total_correct": 0,  # all-time correct answers
        "total_answered": 0,  # all-time attempted answers
        "tests_started": 0,  # games opened from menu
        "total_time_spent_seconds": 0,  # total play time
        "longest_unlimited_streak": 0,  # best streak in endless mode
        "mode_counts": {
            "addition": 0,
            "subtraction": 0,
            "multiplication": 0,
            "division": 0,
            "mixed": 0,
        },
        "most_played_game_mode": "none",  # filled later by counts
        "difficulty_stats": {
            "easy": make_blank_bucket(),
            "medium": make_blank_bucket(),
            "hard": make_blank_bucket(),
        },
        "time_mode_stats": {
            "30": make_blank_bucket(),
            "60": make_blank_bucket(),
            "90": make_blank_bucket(),
            "120": make_blank_bucket(),
            "unlimited": make_blank_bucket(),
        },
        "game_mode_stats": {
            "addition": make_blank_bucket(),
            "subtraction": make_blank_bucket(),
            "multiplication": make_blank_bucket(),
            "division": make_blank_bucket(),
            "mixed": make_blank_bucket(),
        },
    }
    save_users(users)  # persist account
    return True, token  # success + session token

def login(username, password):
    """Log in an existing user and return a fresh token."""
    users = load_users()  # read user database

    if username not in users:  # unknown account
        return False, "Username not found"  # clear feedback

    if users[username]["password"] != scramble_password(password):  # compare hashes
        return False, "Incorrect password"  # wrong login

    # refresh token every login so old sessions cannot be reused
    token = secrets.token_hex(16)  # new token every login
    users[username]["token"] = token  # replace old token
    save_users(users)  # write updated session
    return True, token  # login success

def find_user(username):
    """Get one user by username, or None if missing."""
    users = load_users()  # pull fresh data from file
    return users.get(username)  # return dict or None

def mark_test_started(username, mode):
    """Track when a player starts a test and which mode they picked."""
    users = load_users()  # get current db
    if username not in users:  # guest or deleted user
        return  # skip tracking

    user = users[username]  # shortcut to user object
    user["tests_started"] += 1  # increment starts counter

    if mode in user["mode_counts"]:  # valid mode key check
        user["mode_counts"][mode] += 1  # count this mode pick
        user["most_played_game_mode"] = max(
            user["mode_counts"],
            key=lambda m: user["mode_counts"][m],
        )  # recompute most used mode

    save_users(users)  # save updated counters

def save_game_stats(
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
    """Save score + accuracy + timing stats after a game ends."""
    users = load_users()  # get all users
    if username not in users:  # ignore missing account
        return

    user = users[username]  # target user data
    user["games_played"] += 1  # finished game count
    user["total_correct"] += correct  # add correct answers
    user["total_answered"] += total_answered  # add attempts
    user["total_time_spent_seconds"] += max(0, int(round(time_spent_seconds)))  # add seconds

    # per difficulty bucket
    if difficulty in user["difficulty_stats"]:  # valid difficulty key
        add_to_bucket(user["difficulty_stats"][difficulty], correct, total_answered)  # update bucket

    time_mode = pick_time_mode_key(time_limit)  # map -1/30/60/etc to key
    # per time mode bucket
    if time_mode in user["time_mode_stats"]:  # valid time key
        add_to_bucket(user["time_mode_stats"][time_mode], correct, total_answered)  # update bucket
    # Only unlimited mode contributes to this streak record.
    if time_mode == "unlimited":  # streak tracking only for endless mode
        user["longest_unlimited_streak"] = max(
            user["longest_unlimited_streak"],
            int(longest_streak_in_test),
        )  # keep best endless streak

    # per math mode bucket
    if mode in user["game_mode_stats"]:  # valid mode key
        add_to_bucket(user["game_mode_stats"][mode], correct, total_answered)  # update bucket

    # keep best score seen so far
    if score > user["high_score"]:  # new pb check
        user["high_score"] = score  # save new high score

    save_users(users)  # persist all stat changes

def find_high_score(username):
    """Return high score for a user, or 0 if user does not exist."""
    user = find_user(username)  # fetch account
    if user:  # found user
        return user["high_score"]  # return saved pb
    return 0  # fallback for missing user