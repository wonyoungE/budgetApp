"""Tests for budget.core."""

from budget.core import (
    add_transaction,
    filter_by_category,
    get_balance,
    load_transactions_from_csv,
)
from pathlib import Path


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


def test_get_balance_returns_sum_of_amounts() -> None:
    """Balance should be the sum of income and expense amounts."""
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        },
        {
            "date": "2026-01-05",
            "type": "지출",
            "category": "의료",
            "description": "한의원",
            "amount": -65990,
            "memo": "카드결제",
        },
        {
            "date": "2026-01-15",
            "type": "수입",
            "category": "기타수입",
            "description": "중고 판매",
            "amount": 135541,
            "memo": "",
        },
        {
            "date": "2026-02-01",
            "type": "수입",
            "category": "급여",
            "description": "월급",
            "amount": 4358625,
            "memo": "",
        },
    ]

    assert get_balance(transactions) == 3448380


def test_get_balance_returns_zero_for_empty_transactions() -> None:
    """An empty transaction list should return zero."""
    assert get_balance([]) == 0


def test_filter_by_category_matches_case_insensitively() -> None:
    """Category filtering should ignore case and use real CSV values."""
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        },
        {
            "date": "2026-01-05",
            "type": "지출",
            "category": "의료",
            "description": "한의원",
            "amount": -65990,
            "memo": "카드결제",
        },
        {
            "date": "2026-01-15",
            "type": "수입",
            "category": "기타수입",
            "description": "중고 판매",
            "amount": 135541,
            "memo": "",
        },
    ]

    filtered = filter_by_category(transactions, "여행")

    assert filtered == [transactions[0]]


def test_filter_by_category_returns_empty_list_when_missing() -> None:
    """Missing categories should return an empty list."""
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        }
    ]

    assert filter_by_category(transactions, "주거") == []


def test_filter_by_category_returns_independent_result() -> None:
    """The filtered result should not depend on mutating the source list."""
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        },
        {
            "date": "2026-01-05",
            "type": "지출",
            "category": "의료",
            "description": "한의원",
            "amount": -65990,
            "memo": "카드결제",
        },
    ]

    filtered = filter_by_category(transactions, "여행")
    transactions.append(
        {
            "date": "2026-01-15",
            "type": "수입",
            "category": "여행",
            "description": "환불",
            "amount": 1000,
            "memo": "",
        }
    )

    assert len(filtered) == 1
    assert filtered[0]["category"] == "여행"


def test_load_transactions_from_csv_reads_step1_data() -> None:
    """CSV loading should parse step1 data and convert amount to int."""
    file_path = Path("data") / "step1_transactions.csv"

    transactions = load_transactions_from_csv(str(file_path))

    assert len(transactions) == 10
    assert transactions[0] == {
        "date": "2026-01-05",
        "type": "지출",
        "category": "식비",
        "description": "점심식사",
        "amount": -12000,
        "memo": "",
    }
    assert isinstance(transactions[0]["amount"], int)
    assert transactions[1]["amount"] == 3500000
    assert transactions[-1]["memo"] == "중고마켓"
