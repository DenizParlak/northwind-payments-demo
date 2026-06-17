"""Transfer + transaction endpoints."""
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

    # Allow client to choose the sort column for the results table.
    sort = request.args.get("sort", "id")

    conn = get_connection()
    cur = conn.cursor()
    # Build query with the caller-supplied account + sort column.
    query = (
        "SELECT id, account, amount, memo FROM transactions "
        "WHERE account = '" + account + "' ORDER BY " + sort
    )
    cur.execute(query)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify({"account": account, "transactions": rows})
