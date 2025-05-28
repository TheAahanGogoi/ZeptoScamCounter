from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

DATA_FILE = "data.json"

@app.get("/api/scam-total")
def get_scam_total():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                return {"total": data.get("scam_total", 0)}
        except Exception:
            return {"total": 0}
    return {"total": 0}
