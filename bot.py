import praw
import json
import os
import re
from datetime import datetime

# Reddit API setup
reddit = praw.Reddit(
    client_id="redacted",
    client_secret="redacted",
    username="redacted",
    password="redacted",
    user_agent="ZeptoScamCounter by u/dawn-the-great"
)

SUBREDDIT = "FuckZepto"
COMMENT_TEXT = "How much were you scammed for?"
DATA_FILE = "data.json"
MAX_AMOUNT = 500

# Load or initialize data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {
        "commented_posts": [],
        "reply_data": {},
        "scam_total": 0
    }

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def comment_on_new_posts():
    subreddit = reddit.subreddit(SUBREDDIT)
    for post in subreddit.new(limit=2):
        if post.id not in data["commented_posts"]:
            try:
                comment = post.reply(COMMENT_TEXT)
                print(f"[{datetime.now()}] Commented on: {post.title}")
                data["commented_posts"].append(post.id)
                data["reply_data"][post.id] = {
                    "comment_id": comment.id,
                    "op": post.author.name,
                    "replied": False
                }
            except Exception as e:
                print(f"Error commenting on {post.id}: {e}")
    save_data()

def parse_amount(text):
    match = re.search(r"(?:₹|\bINR\s?)?(\d{1,4})", text)
    if match:
        amount = int(match.group(1))
        return min(amount, MAX_AMOUNT)
    return None

def check_replies():
    for post_id, info in data["reply_data"].items():
        if info["replied"]:
            continue

        try:
            comment = reddit.comment(id=info["comment_id"])
            comment.refresh()  # Ensure we get all replies

            for reply in comment.replies:
                if reply.author and reply.author.name == info["op"]:
                    amount = parse_amount(reply.body)
                    if amount:
                        print(f"[{datetime.now()}] OP replied with ₹{amount} on post {post_id}")
                        data["scam_total"] += amount
                        info["replied"] = True
                        save_data()
                        break  # Only count the first valid reply
        except Exception as e:
            print(f"Error checking replies for post {post_id}: {e}")

if __name__ == "__main__":
    comment_on_new_posts()
    check_replies()
