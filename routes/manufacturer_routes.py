from flask import Blueprint, request, render_template, session, redirect, flash, get_flashed_messages
from services.product_service import get_product_types, save_product, add_product_type, get_all_products
import sqlite3

manufacturer = Blueprint('manufacturer', __name__)

@manufacturer.route('/add-product-type', methods=['POST'])
def add_product():

    from flask import request, redirect, session

    if not session.get('user_email'):
        flash("Please login first", "error")
        return redirect('/login')

    if session.get('role') != 'manufacturer':
        flash("Unauthorized access", "error")
        return redirect('/login')

    new_product = request.form.get('newProduct')

    if not new_product:
        flash("Invalid product name", "error")
        return redirect('/manufacturer')

    add_product_type(new_product, session.get('user_email'))
    flash("Product type added successfully!", "success")
    return redirect('/manufacturer') 

@manufacturer.route('/manufacturer', methods=['GET', 'POST'])
def manufacturer_page():
    email = session.get('user_email')
    products = get_product_types(session.get('user_email'))
    print("Session email:", email)
    stored_products = get_all_products(email)
    print("stored products:", stored_products)
    if request.method == 'GET':
        return render_template("manufacturer.html", products=products, stored_products=stored_products)
    if session.get('role') != 'manufacturer':
        flash("Not a Manufacturer, unauthorized access", "error")
        return redirect('/login')

    data = request.form
    if request.method == 'POST':
        itemId = data.get('itemId')
        product_type_id = data.get('productDropdown')
        metadataHash = data.get('metadataHash')

        if not email:
            flash("User not logged in", "error")
            return redirect('/login')

        if not all([itemId, product_type_id, metadataHash]):
            flash("All fields are required", "error")
            return redirect('/manufacturer')

        save_product(itemId, product_type_id, metadataHash, email)
        flash("Product saved successfully!", "success")
        return redirect('/manufacturer')

    return render_template(
        "manufacturer.html",
        products=products,
        stored_products=stored_products
    )

@manufacturer.route('/delete-item', methods=['POST'])
def delete_item():
    item_id = request.form['itemId']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE itemId = ?", (item_id,))
    conn.commit()
    conn.close()

    flash("Item deleted successfully!", "success")
    return redirect('/manufacturer')

@manufacturer.route('/delete-product-type', methods=['POST'])
def delete_product_type():
    product = request.form['product']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE product_types SET is_active = 0 WHERE name = ?",
        (product,)
    )

    conn.commit()
    conn.close()

    flash("Product type removed!", "success")
    return redirect('/manufacturer')