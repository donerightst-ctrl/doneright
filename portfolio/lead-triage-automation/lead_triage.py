import json
import sys
from pathlib import Path


def normalize_lead(raw):
    required = ("name", "email")
    missing = [key for key in required if not str(raw.get(key, "")).strip()]
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")

    email = str(raw["email"]).strip().lower()
    if "@" not in email:
        raise ValueError("invalid email")

    return {
        "name": str(raw["name"]).strip(),
        "email": email,
        "company": str(raw.get("company", "")).strip(),
        "source": str(raw.get("source", "unknown")).strip().lower(),
        "message": str(raw.get("message", "")).strip(),
        "budget": float(raw.get("budget") or 0),
    }


def score_lead(lead):
    score = 0
    reasons = []

    if lead["company"]:
        score += 15
        reasons.append("company supplied")
    if lead["budget"] >= 1000:
        score += 35
        reasons.append("budget >= 1000")
    elif lead["budget"] > 0:
        score += 15
        reasons.append("budget supplied")

    high_intent = ("demo", "quote", "price", "integration", "automation")
    message = lead["message"].lower()
    matches = [term for term in high_intent if term in message]
    if matches:
        score += min(30, 10 * len(matches))
        reasons.append("high-intent message")

    if lead["source"] in {"referral", "partner", "inbound"}:
        score += 20
        reasons.append("high-quality source")

    score = min(score, 100)
    tier = "hot" if score >= 60 else "warm" if score >= 30 else "cold"
    return {**lead, "score": score, "tier": tier, "reasons": reasons}


def triage(items):
    scored = []
    errors = []
    for index, raw in enumerate(items):
        try:
            scored.append(score_lead(normalize_lead(raw)))
        except (TypeError, ValueError) as exc:
            errors.append({"index": index, "error": str(exc)})
    scored.sort(key=lambda item: (-item["score"], item["email"]))
    return {"leads": scored, "errors": errors}


def main():
    if len(sys.argv) > 2:
        raise SystemExit("usage: python lead_triage.py [leads.json]")

    if len(sys.argv) == 2:
        payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    else:
        payload = json.load(sys.stdin)

    if not isinstance(payload, list):
        raise SystemExit("input must be a JSON array")

    json.dump(triage(payload), sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
