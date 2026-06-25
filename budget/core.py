"""Core functions for the budget CLI app."""

from csv import DictReader
from pathlib import Path
from typing import Any


def add_transaction(
    transactions: list[dict[str, Any]],
    transaction: dict[str, Any],
) -> list[dict[str, Any]]:
    """Add a transaction to the budget data and return the updated list."""
    return transactions + [transaction]


def get_balance(transactions: list[dict[str, Any]]) -> int:
    """Return the current balance."""
    return sum(transaction["amount"] for transaction in transactions)


def filter_by_category(
    transactions: list[dict[str, Any]],
    category: str,
) -> list[dict[str, Any]]:
    """Filter transactions by category."""
    return [
        transaction
        for transaction in transactions
        if transaction["category"].lower() == category.lower()
    ]


def load_transactions_from_csv(file_path: str) -> list[dict[str, Any]]:
    """Load transactions from a CSV file."""
    path = Path(file_path)

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = DictReader(file)
        return [
            {
                "date": row["date"],
                "type": row["type"],
                "category": row["category"],
                "description": row["description"],
                "amount": int(row["amount"]),
                "memo": row["memo"],
            }
            for row in reader
        ]


def monthly_summary(
    transactions: list[dict[str, Any]],
) -> dict[str, dict[str, int]]:
    """Summarize transactions by month."""
    summary: dict[str, dict[str, int]] = {}

    for transaction in transactions:
        month = transaction["date"][:7]
        if month not in summary:
            summary[month] = {"income": 0, "expense": 0, "net": 0}

        amount = transaction["amount"]
        if amount >= 0:
            summary[month]["income"] += amount
        else:
            summary[month]["expense"] += amount
        summary[month]["net"] += amount

    return summary
