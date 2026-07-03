from flask import Flask, jsonify, request

app = Flask(__name__)

# ─────────────────────────────────────────
#  In-memory "database"  (same as before)
# ─────────────────────────────────────────
transactions = []
next_id = 1          # simple auto-increment ID for each transaction


# ─────────────────────────────────────────
#  Helper
# ─────────────────────────────────────────
def get_category(litres: int) -> str:
    if litres < 20:
        return "Small Fill"
    elif litres <= 49:
        return "Regular Fill"
    else:
        return "Large Fill"


# ─────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────

# CREATE — POST /transactions
# Mirrors recordT()
@app.route("/transactions", methods=["POST"])
def create_transaction():
    global next_id
    data = request.get_json()

    # basic validation
    required = ["vehicle_no", "fuel_type", "litre_dispensed"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    transaction = {
        "id":              next_id,
        "vehicle_no":      data["vehicle_no"],
        "fuel_type":       data["fuel_type"],
        "litre_dispensed": int(data["litre_dispensed"]),
        "category":        get_category(int(data["litre_dispensed"])),
    }
    transactions.append(transaction)
    next_id += 1

    return jsonify(transaction), 201        # 201 = Created


# READ ALL — GET /transactions
# Mirrors displayAll()
@app.route("/transactions", methods=["GET"])
def get_all_transactions():
    return jsonify(transactions), 200


# READ ONE — GET /transactions/<id>
# Get a single transaction by its ID
@app.route("/transactions/<int:transaction_id>", methods=["GET"])
def get_transaction(transaction_id):
    transaction = next((t for t in transactions if t["id"] == transaction_id), None)

    if transaction is None:
        return jsonify({"error": "Transaction not found"}), 404   # 404 = Not Found

    return jsonify(transaction), 200


# UPDATE — PUT /transactions/<id>
# Update any field of an existing transaction
@app.route("/transactions/<int:transaction_id>", methods=["PUT"])
def update_transaction(transaction_id):
    transaction = next((t for t in transactions if t["id"] == transaction_id), None)

    if transaction is None:
        return jsonify({"error": "Transaction not found"}), 404

    data = request.get_json()

    # update only the fields that were sent
    if "vehicle_no" in data:
        transaction["vehicle_no"] = data["vehicle_no"]
    if "fuel_type" in data:
        transaction["fuel_type"] = data["fuel_type"]
    if "litre_dispensed" in data:
        transaction["litre_dispensed"] = int(data["litre_dispensed"])
        transaction["category"] = get_category(int(data["litre_dispensed"]))

    return jsonify(transaction), 200


# DELETE — DELETE /transactions/<id>
# Remove a transaction from the list
@app.route("/transactions/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    global transactions
    transaction = next((t for t in transactions if t["id"] == transaction_id), None)

    if transaction is None:
        return jsonify({"error": "Transaction not found"}), 404

    transactions = [t for t in transactions if t["id"] != transaction_id]
    return jsonify({"message": f"Transaction {transaction_id} deleted"}), 200


# BONUS — GET /transactions/summary
# Mirrors summary()
@app.route("/transactions/summary", methods=["GET"])
def get_summary():
    if not transactions:
        return jsonify({"message": "No transactions recorded yet"}), 200

    total_litres = sum(t["litre_dispensed"] for t in transactions)
    return jsonify({
        "total_transactions": len(transactions),
        "total_litres":       total_litres,
        "average_litres":     round(total_litres / len(transactions), 2),
    }), 200


# BONUS — GET /transactions/large-fills
# Mirrors findALFT()
@app.route("/transactions/large-fills", methods=["GET"])
def get_large_fills():
    large = [t for t in transactions if t["category"] == "Large Fill"]
    return jsonify(large), 200


# ─────────────────────────────────────────
#  Run the server
# ─────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
