# Import libraries
from flask import Flask, render_template, request, url_for, redirect

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route("/", methods=['GET'])
def get_transactions():
    balance = sum(t['amount'] for t in transactions)
    return render_template("transactions.html", transactions=transactions, balance=balance)
# Create operation
@app.route("/add", methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        transation = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        transactions.append(transation)
        return redirect(url_for('get_transactions'))

    return render_template("form.html")


# Update operation: Display edit transaction form
# Route to handle the editing of an existing transaction
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Extract the updated values from the form fields
        date = request.form['date']  # Get the 'date' field value from the form
        amount = float(request.form['amount'])  # Get the 'amount' field value from the form and convert it to a float

        # Find the transaction with the matching ID and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date  # Update the 'date' field of the transaction
                transaction['amount'] = amount  # Update the 'amount' field of the transaction
                break  # Exit the loop once the transaction is found and updated

        # Redirect to the transactions list page after updating the transaction
        return redirect(url_for("get_transactions"))

    # If the request method is GET, find the transaction with the matching ID and render the edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            # Render the edit form template and pass the transaction to be edited
            return render_template("edit.html", transaction=transaction)

    # If the transaction with the specified ID is not found, handle this case (optional)
    return {"message": "Transaction not found"}, 404

# Delete operation: Delete a transaction
# Route to handle the deletion of an existing transaction
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Find the transaction with the matching ID and remove it from the list
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)  # Remove the transaction from the transactions list
            break  # Exit the loop once the transaction is found and removed

    # Redirect to the transactions list page after deleting the transaction
    return redirect(url_for("get_transactions"))

# ✅ Neue Suche-Route
@app.route("/search", methods=['GET', 'POST'])
def search_transactions():
    if request.method == 'POST':
        # Werte aus dem Formular lesen und zu float konvertieren
        min_amount = float(request.form['min_amount'])
        max_amount = float(request.form['max_amount'])

        # List-Comprehension zum Filtern
        filtered_transactions = [
            t for t in transactions
            if min_amount <= t['amount'] <= max_amount
        ]

        # Gefilterte Liste an die bestehende Template-Ansicht übergeben
        return render_template("transactions.html", transactions=filtered_transactions)

    # Bei GET: Suchformular anzeigen
    return render_template("search.html")

# ✅ TOTAL Balance
@app.route("/balance")
def total_balance():
    balance = 0
    for i in transactions:
        balance += i['amount']

    return f"Total Balance: {balance}"

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)