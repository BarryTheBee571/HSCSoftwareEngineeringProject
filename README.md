# Speedy Maths

A Python desktop maths practice game for students, built with CustomTkinter.

## Overview

This project is a timed maths game designed for practising basic arithmetic skills. It supports:
- account login, registration, and guest play
- selectable game modes: addition, subtraction, multiplication, division, mixed
- selectable difficulty: easy, medium, hard
- selectable time limits and unlimited mode
- score tracking, accuracy feedback, and streaks
- account statistics and leaderboard for registered users

## Requirements

- Python 3.8+ (Python 3.10+ recommended)
- `customtkinter`

## Install
Open a terminal in the project root and run:

```
pip install customtkinter
```

## Run

Run the main.py file in the Project Folder

## Notes

- User accounts are stored locally in `Project/users.json`.
- Passwords are hashed before storage.
- Guest mode does not save statistics.