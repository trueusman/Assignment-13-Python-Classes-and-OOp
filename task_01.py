"""Task 01: Nested Transaction Analyzer."""


def analyze_transactions(transactions):
    seen_ids = set()
    customers = {}

    for transaction in transactions:
        required = {"id", "customer", "category", "amount", "status"}
        if not isinstance(transaction, dict) or not required.issubset(transaction):
            raise ValueError("Each transaction must contain id, customer, category, amount, status")

        transaction_id = transaction["id"]
        if transaction_id in seen_ids:
            raise ValueError(f"Duplicate transaction ID: {transaction_id}")
        seen_ids.add(transaction_id)

        customer = transaction["customer"]
        if not isinstance(customer, str) or not customer:
            raise ValueError("Customer name must be a non-empty string")

        customers.setdefault(customer, {"total": 0, "categories": {}})
        if transaction["status"] != "success":
            continue

        amount = transaction["amount"]
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount < 0:
            raise ValueError("Transaction amount must be a non-negative number")

        category = transaction["category"]
        categories = customers[customer]["categories"]
        customers[customer]["total"] += amount
        categories[category] = categories.get(category, 0) + amount

    report = []
    for customer, totals in customers.items():
        categories = totals["categories"]
        top_category = None
        if categories:
            top_category = sorted(
                categories,
                key=lambda category: (-categories[category], category),
            )[0]

        report.append({
            "customer": customer,
            "total": totals["total"],
            "top_category": top_category,
        })

    report.sort(key=lambda row: (-row["total"], row["customer"]))
    for rank, row in enumerate(report, start=1):
        row["rank"] = rank
    return report


if __name__ == "__main__":
    sample = [
        {"id": 1, "customer": "Ali", "category": "Food", "amount": 500, "status": "success"},
        {"id": 2, "customer": "Ali", "category": "Travel", "amount": 200, "status": "failed"},
        {"id": 3, "customer": "Sara", "category": "Food", "amount": 700, "status": "success"},
    ]
    for row in analyze_transactions(sample):
        print(row)
