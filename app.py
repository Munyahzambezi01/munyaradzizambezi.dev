import os
from flask import Flask, render_template, request, redirect
from cs50 import SQL

# Configure app
app = Flask(__name__)

# Connect to database
db = SQL("sqlite:///Menu.db")

@app.route("/")
def index():
    # Fetch menu items from the database
    menu = db.execute("SELECT * FROM Menu")
    return render_template("menu.html", menu=menu)

@app.route("/order", methods=["POST"])
def order():
    # Process order submission
    item_id = request.form.get("item_id")
    item_name = request.form.get("item_name")
    quantity = request.form.get("quantity")

    # Fetch item_name from Menu table based on item_id
    item_name_result = db.execute("SELECT item_name FROM Menu WHERE id = :item_id", item_id=item_id)

    # Check if the result contains any rows
    if item_name_result:
        item_name = item_name_result[0]["item_name"]
    else:
        # Handle the case where no item is found for the given item_id
        item_name = None

    # Insert the order into the database
    db.execute("INSERT INTO orders (item_id, item_name, quantity) VALUES (:item_id, :item_name, :quantity)",
               item_id=item_id, item_name=item_name, quantity=quantity)

    return redirect("/order_confirmation")

@app.route("/order_confirmation")
def order_confirmation():
    # Fetch orders from the database with item names
    orders = db.execute("SELECT o.id AS order_id, m.item_name, o.quantity, o.status FROM Orders o JOIN Menu m ON o.item_id = m.id")
    return render_template("order_confirmation.html", orders=orders)

if __name__ == "__main__":
    app.run(debug=True)
