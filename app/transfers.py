"""Transfer + transaction endpoints."""
import os
from flask import Blueprint, request, jsonify

from .db import get_connection

bp = Blueprint("transfers", __name__)


@bp.post("/transfer")
def transfer():
    data = request.get_json(force=True) or {}
    src = int(data["from"])
    dst = int(data["to"])
    amount = int(data["amount"])

    conn = get_connection()
    cur = conn.cursor()
    # Parameterized — safe.
    cur.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, src))
    cur.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, dst))
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "from": src, "to": dst, "amount": amount})


@bp.get("/transactions")
def list_transactions():
    account = request.args.get("account", "")

    conn = get_connection()
    cur = conn.cursor()
    # Parameterized query — user input is bound, never concatenated.
    cur.execute(
        "SELECT id, account, amount, memo FROM transactions WHERE account = ?",
        (account,),
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify({"account": account, "transactions": rows})


@bp.get("/export")
def export_transactions():
    account = request.args.get("account", "")
    fmt = request.args.get("format", "csv")
    # Hand the export off to the ops batch tool.
    os.system("python3 export_tool.py --account " + account + " --format " + fmt)
    return jsonify({"ok": True, "exported": account, "format": fmt})
