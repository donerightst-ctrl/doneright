import hashlib
import json
import os
import sqlite3
import urllib.request
from contextlib import closing
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel, EmailStr, Field

DB_PATH = os.getenv("DB_PATH", "leads.sqlite3")
WEBHOOK_URL = os.getenv("NOTIFY_WEBHOOK_URL", "").strip()

app = FastAPI(title="Lead Capture Automation", version="1.0.0")


class LeadCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    phone: Optional[str] = Field(default=None, max_length=60)
    service: str = Field(min_length=1, max_length=120)
    message: str = Field(min_length=1, max_length=4000)


class LeadResult(BaseModel):
    id: int
    duplicate: bool
    notified: bool


def _connect(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DB_PATH) -> None:
    with _connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                fingerprint TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                service TEXT NOT NULL,
                message TEXT NOT NULL
            )
            """
        )
        conn.commit()


def _fingerprint(lead: LeadCreate) -> str:
    canonical = "|".join(
        [
            lead.email.strip().lower(),
            (lead.phone or "").strip(),
            lead.service.strip().lower(),
            lead.message.strip(),
        ]
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def save_lead(lead: LeadCreate, db_path: str = DB_PATH) -> tuple[int, bool]:
    init_db(db_path)
    fp = _fingerprint(lead)
    now = datetime.now(timezone.utc).isoformat()

    with _connect(db_path) as conn:
        try:
            cur = conn.execute(
                """
                INSERT INTO leads
                    (created_at, fingerprint, name, email, phone, service, message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    now,
                    fp,
                    lead.name.strip(),
                    lead.email.strip().lower(),
                    (lead.phone or "").strip() or None,
                    lead.service.strip(),
                    lead.message.strip(),
                ),
            )
            conn.commit()
            return int(cur.lastrowid), False
        except sqlite3.IntegrityError:
            row = conn.execute(
                "SELECT id FROM leads WHERE fingerprint = ?", (fp,)
            ).fetchone()
            if row is None:
                raise
            return int(row["id"]), True


def list_leads(limit: int = 50, db_path: str = DB_PATH) -> list[dict]:
    init_db(db_path)
    with closing(_connect(db_path)) as conn:
        rows = conn.execute(
            """
            SELECT id, created_at, name, email, phone, service, message
            FROM leads
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def notify_webhook(lead_id: int, lead: LeadCreate, webhook_url: str = WEBHOOK_URL) -> bool:
    if not webhook_url:
        return False

    payload = json.dumps(
        {
            "event": "new_lead",
            "lead_id": lead_id,
            "name": lead.name,
            "email": str(lead.email),
            "phone": lead.phone,
            "service": lead.service,
            "message": lead.message,
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            return 200 <= response.status < 300
    except Exception:
        return False


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/leads", response_model=LeadResult)
def create_lead(lead: LeadCreate) -> LeadResult:
    lead_id, duplicate = save_lead(lead)
    notified = False if duplicate else notify_webhook(lead_id, lead)
    return LeadResult(id=lead_id, duplicate=duplicate, notified=notified)


@app.get("/leads")
def recent_leads(limit: int = Query(default=50, ge=1, le=200)) -> list[dict]:
    return list_leads(limit=limit)
