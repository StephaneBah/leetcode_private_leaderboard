# LeetCode Private Leaderboard

This repository contains a small Flask app for a private LeetCode leaderboard. It relies on the public API hosted at [alfa-leetcode-api](https://github.com/alfaarghya/alfa-leetcode-api).

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   python leaderboard.py
   ```

The application automatically creates a SQLite database (`leaderboard.db`) to store registered users.

Open `http://localhost:5000/` to view the leaderboard and add your LeetCode ID.

The page now uses [Bootstrap](https://getbootstrap.com/) for a cleaner table and form design. Each row displays the user's total solved problems and their public LeetCode ranking when available.
