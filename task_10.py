"""Task 10: Reconcile inventory CSV with stock movements."""

import csv

def reconcile_inventory(inventory_path, movements_path,
                        updated_path="updated_inventory.csv",
                        rejected_path="rejected_movements.csv"):
    stock = {}
    names = {}
    with open(inventory_path, newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            sku = row["sku"].strip()
            quantity = int(row["quantity"])
            if quantity < 0 or sku in stock:
                raise ValueError(f"Invalid or duplicate inventory row: {sku}")
            stock[sku] = quantity
            names[sku] = row["name"]

    rejected = []
    with open(movements_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for line_number, row in enumerate(reader, start=2):
            sku = (row.get("sku") or "").strip()
            movement_type = (row.get("type") or "").strip().upper()
            try:
                units = int(row.get("units", ""))
                if units <= 0:
                    raise ValueError("units must be positive")
                if sku not in stock:
                    raise ValueError("unknown SKU")
                if movement_type == "IN":
                    stock[sku] += units
                elif movement_type == "OUT":
                    if stock[sku] - units < 0:
                        raise ValueError("insufficient stock")
                    stock[sku] -= units
                else:
                    raise ValueError("type must be IN or OUT")
            except (ValueError, TypeError) as exc:
                rejected.append({
                    "line_number": line_number,
                    "sku": sku,
                    "type": movement_type,
                    "units": row.get("units", ""),
                    "reason": str(exc)
                })

    with open(updated_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["sku", "name", "quantity"])
        writer.writeheader()
        for sku, quantity in stock.items():
            writer.writerow({"sku": sku, "name": names[sku], "quantity": quantity})

    with open(rejected_path, "w", newline="", encoding="utf-8") as file:
        fields = ["line_number", "sku", "type", "units", "reason"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rejected)

    return stock, rejected


if __name__ == "__main__":
    # Create sample input files if they do not exist.
    with open("inventory.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["sku", "name", "quantity"])
        w.writerow(["P01", "Notebook", 10])
    with open("movements.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["sku", "type", "units"])
        w.writerows([["P01", "OUT", 4], ["P01", "OUT", 9], ["P01", "IN", 2]])
    print(reconcile_inventory("inventory.csv", "movements.csv"))
