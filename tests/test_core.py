"""Tests for budget.core."""

from budget.core import add_transaction


def test_add_transaction_increases_length() -> None:
    """Adding a transaction should increase the transaction count."""
    transactions = [
        {
            "date": "2026-01-05",
            "type": "지출",
            "category": "식비",
            "description": "점심식사",
            "amount": -12000,
            "memo": "",
        }
    ]

    transaction = {
        "date": "2026-01-07",
        "type": "수입",
        "category": "급여",
        "description": "월급",
        "amount": 3500000,
        "memo": "1월급여",
    }

    updated_transactions = add_transaction(transactions, transaction)

    assert len(updated_transactions) == 2


def test_add_transaction_preserves_negative_amount() -> None:
    """A negative amount should be stored as an expense."""
    transactions = []
    transaction = {
        "date": "2026-01-10",
        "type": "지출",
        "category": "교통",
        "description": "지하철",
        "amount": -1500,
        "memo": "",
    }

    updated_transactions = add_transaction(transactions, transaction)

    assert updated_transactions[0]["amount"] == -1500
    assert updated_transactions[0]["type"] == "지출"


def test_add_transaction_preserves_positive_amount() -> None:
    """A positive amount should be stored as income."""
    transactions = []
    transaction = {
        "date": "2026-01-07",
        "type": "수입",
        "category": "급여",
        "description": "월급",
        "amount": 3500000,
        "memo": "1월급여",
    }

    updated_transactions = add_transaction(transactions, transaction)

    assert updated_transactions[0]["amount"] == 3500000
    assert updated_transactions[0]["type"] == "수입"


def test_add_transaction_allows_empty_description() -> None:
    """An empty description should be handled without failure."""
    transactions = []
    transaction = {
        "date": "2026-01-12",
        "type": "지출",
        "category": "식비",
        "description": "",
        "amount": -5800,
        "memo": "",
    }

    updated_transactions = add_transaction(transactions, transaction)

    assert updated_transactions[0]["description"] == ""
