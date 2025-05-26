# 🧾 Zepto Scam Counter

A passive data-collection system powered by Reddit user interaction. This project tracks how much money users report being scammed by Zepto, using a fully automated Reddit bot + minimal backend infrastructure.

---

## 🚀 Overview

This system monitors posts on [`r/FuckZepto`](https://reddit.com/r/FuckZepto) and asks the original poster:

> “How much were you scammed for?”

If the OP replies with a valid ₹ amount (e.g. `₹200`, `100`), the bot parses it, caps it (e.g. at ₹500), and adds it to a running total. The total is then served via an API and displayed on a public website.

---

## ⚙️ How It Works

- **Bot (PRAW + Python):**
  - Monitors subreddit for new posts
  - Comments on each post
  - Tracks OP replies and parses ₹ values
  - Stores post IDs, usernames, reply IDs, and total in a `data.json` file

- **Backend (FastAPI):**
  - Serves the total via `/api/scam-total`

- **Frontend (HTML + JS):**
  - Displays live scam total
  - Hosted free on GitHub Pages 

---
