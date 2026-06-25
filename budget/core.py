"""Core functions for the budget CLI app."""

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


def filter_by_category() -> None:
    """Filter transactions by category."""
    pass


def load_transactions_from_csv() -> None:
    """Load transactions from a CSV file."""
    pass


def monthly_summary() -> None:
    """Summarize transactions by month."""
    pass
