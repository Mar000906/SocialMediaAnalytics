## ✨ Project Overview

🚀 Social Media Analytics Tool is a Python-powered application designed to make social media data analysis simple and interactive.

📊 With this tool, you can:

🔢 Track total posts, likes, comments, and shares

🌟 Identify your top-performing posts

🏷️ Discover the most popular hashtags

📈 Visualize everything through a user-friendly dashboard

💡 This project is designed to simplify social media data analysis, making it easier for users to monitor trends, measure engagement, and make data-driven decisions.

----- 

## 🛠️ Technologies Used

🐍 Python 3.10+ – Core programming language

⚡ Flask – For building the web application

🌿 python-dotenv – Manage environment variables

🧠 VADER Sentiment – Sentiment analysis on social media content

📊 Matplotlib / Plotly – For data visualization and charts

📦 pip & virtualenv – Package and environment management


------


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

----

## 👤 Author

Name: Marwa Halli

📧 Email: marwa.halli@uit.ac.ma

💼 LinkedIn: www.linkedin.com/in/marwa-halli000
