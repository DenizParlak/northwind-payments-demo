# northwind-payments-demo

Internal payments service for Northwind Bank (demo).

A small Flask API that moves money between accounts and looks up transactions.
Security-gated by **TraceMint / Thor** on every pull request — a new critical
finding (e.g. a SQL-injection sink) blocks the merge.

## Run

```bash
pip install -r requirements.txt
python -m app
```

## Endpoints

- `POST /transfer` — move funds between two accounts
- `GET  /transactions?account=<id>` — list a customer's transactions
