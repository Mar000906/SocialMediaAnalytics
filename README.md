# Social Media Analytics Tool (Starter)

Minimal starter using **Python (Flask)**, **SQLite (SQL)**, **HTML**, and **CSS**.  
Upload a CSV of posts, store them in DB, compute **engagement** and **sentiment**, and show a basic dashboard.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python app.py
# Visit http://127.0.0.1:5000
```

## CSV Columns
Required: `platform, post_id, author, content, created_at, likes, comments, shares, views, followers`.  
Optional: `url`.

Engagement rate: `(likes + comments + shares) / max(1, followers)`  
Sentiment: VADER compound score in [-1, 1].
