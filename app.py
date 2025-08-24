\
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from db import init_db, bulk_insert_posts, query_one, query_all
from utils import compute_sentiment, compute_engagement_row, extract_hashtags

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_key")
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(UPLOAD_DIR, exist_ok=True)

init_db()

def parse_date(s):
    # Try a couple of formats
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            pass
    # Fallback: now
    return datetime.utcnow()

@app.route("/")
def index():
    # KPIs
    totals = query_one(
        '''SELECT COUNT(*), COALESCE(SUM(likes),0), COALESCE(SUM(comments),0), COALESCE(SUM(shares),0), COALESCE(AVG(engagement_rate),0)
           FROM posts'''
    )
    total_posts, sum_likes, sum_comments, sum_shares, avg_eng = totals or (0,0,0,0,0.0)

    # Top posts by engagement
    top_posts = query_all(
        '''SELECT platform, author, content, likes, comments, shares, followers, engagement_rate, url, created_at
           FROM posts
           ORDER BY engagement_rate DESC
           LIMIT 10'''
    )

    # Top hashtags (simple)
    hashtag_rows = query_all('''SELECT content FROM posts WHERE content IS NOT NULL''')
    from collections import Counter
    counter = Counter()
    for (content,) in hashtag_rows:
        for h in extract_hashtags(content):
            counter[h] += 1
    top_hashtags = counter.most_common(10)

    # Recent posts
    recent = query_all(
        '''SELECT platform, author, content, likes, comments, shares, engagement_rate, created_at
           FROM posts ORDER BY datetime(created_at) DESC LIMIT 10'''
    )

    return render_template("index.html",
                           total_posts=total_posts,
                           sum_likes=sum_likes,
                           sum_comments=sum_comments,
                           sum_shares=sum_shares,
                           avg_eng=avg_eng,
                           top_posts=top_posts,
                           top_hashtags=top_hashtags,
                           recent=recent)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            flash("Choisis un fichier CSV.")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_DIR, filename)
        file.save(path)

        # Parse CSV
        import csv
        rows = []
        with open(path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            required = {"platform","post_id","author","content","created_at","likes","comments","shares","views","followers"}
            if not required.issubset(set([h.strip() for h in reader.fieldnames or []])):
                flash("Le CSV doit contenir les colonnes: " + ", ".join(sorted(required)))
                return redirect(request.url)

            for r in reader:
                platform = (r.get("platform") or "").strip().lower()
                post_id = (r.get("post_id") or "").strip()
                author = (r.get("author") or "").strip()
                content = (r.get("content") or "").strip()
                created_at = (r.get("created_at") or "").strip()
                likes = int(r.get("likes") or 0)
                comments = int(r.get("comments") or 0)
                shares = int(r.get("shares") or 0)
                views = int(r.get("views") or 0)
                followers = int(r.get("followers") or 0)
                url = (r.get("url") or "").strip()

                # Compute analytics
                sentiment = compute_sentiment(content)
                engagement = compute_engagement_row(likes, comments, shares, followers)

                # Normalize date to ISO string
                dt = parse_date(created_at)
                created_at_iso = dt.strftime("%Y-%m-%d %H:%M:%S")

                rows.append((platform, post_id, author, content, created_at_iso,
                             likes, comments, shares, views, followers, url, sentiment, engagement))

        if rows:
            bulk_insert_posts(rows)
            flash(f"Import réussi: {len(rows)} posts ajoutés.")
            return redirect(url_for("index"))
        else:
            flash("Aucune ligne valide trouvée.")
            return redirect(request.url)

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "true").lower() == "true")
