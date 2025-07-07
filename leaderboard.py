import os
import sqlite3
import requests
from flask import Flask, request, redirect, render_template, g

DB_PATH = 'leaderboard.db'
app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY)')
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def get_users():
    cur = get_db().execute('SELECT username FROM users')
    rows = cur.fetchall()
    return [r[0] for r in rows]

def add_user_db(username):
    db = get_db()
    db.execute('INSERT OR IGNORE INTO users (username) VALUES (?)', (username,))
    db.commit()


def fetch_user_stats(username):
    url = f"https://alfa-leetcode-api.vercel.app/api/{username}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return {
        'username': username,
        'totalSolved': data.get('totalSolved', 0),
        'ranking': data.get('ranking')
    }


def update_stats(users):
    stats = []
    for user in users:
        try:
            stats.append(fetch_user_stats(user))
        except Exception:
            continue
    return sorted(stats, key=lambda x: x['totalSolved'], reverse=True)


@app.route('/', methods=['GET'])
def leaderboard():
    users = get_users()
    stats = update_stats(users)
    return render_template('leaderboard.html', stats=stats)


@app.route('/add', methods=['POST'])
def add_user():
    username = request.form.get('username')
    if username:
        add_user_db(username)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
