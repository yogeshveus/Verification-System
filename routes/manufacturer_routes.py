from flask import Blueprint, request, render_template, session, redirect, flash, get_flashed_messages, jsonify, current_app
from services.product_service import get_product_types, save_product, add_product_type, get_all_products
import sqlite3
from config import DATABASE
import os
import json

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
        return redirect('/manufacturer/item')

    add_product_type(new_product, session.get('user_email'))
    flash("Product type added successfully!", "success")
    return redirect('/manufacturer/item') 

@manufacturer.route('/manufacturer/item', methods=['GET', 'POST'])
def manufacturer_page():
    if session.get('role') != 'manufacturer':
        flash("Not a Manufacturer, unauthorized access", "error")
        return redirect('/login')
    email = session.get('user_email')
    products = get_product_types(session.get('user_email'))
    stored_products = get_all_products(email)
    if request.method == 'GET':
        return render_template("manufacturer/manufacturer_item.html", products=products, stored_products=stored_products)

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
            return redirect('/manufacturer/item')

        save_product(itemId, product_type_id, metadataHash, email)
        flash("Product saved successfully!", "success")
        return redirect('/manufacturer/item')

    return render_template(
        "manufacturer/manufacturer_item.html",
        products=products,
        stored_products=stored_products
    )

@manufacturer.route('/delete-item', methods=['POST'])
def delete_item():
    if session.get('role') != 'manufacturer':
        flash("Unauthorized access", "error")
        return redirect('/login')
    item_id = request.form['itemId']

    #conn = sqlite3.connect(DATABASE)
    conn = sqlite3.connect(current_app.config['DATABASE'])
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE itemId = ?", (item_id,))
    conn.commit()
    conn.close()

    flash("Item deleted successfully!", "success")
    return redirect('/manufacturer/item')

@manufacturer.route('/delete-product-type', methods=['POST'])
def delete_product_type():
    if session.get('role') != 'manufacturer':
        flash("Unauthorized access", "error")
        return redirect('/login')
    product = request.form['product']

    #conn = sqlite3.connect(DATABASE)
    conn = sqlite3.connect(current_app.config['DATABASE'])
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE product_types SET is_active = 0 WHERE name = ?",
        (product,)
    )

    conn.commit()
    conn.close()

    flash("Product type removed!", "success")
    return redirect('/manufacturer/item')

@manufacturer.route('/manufacturer')
def manufacturer_home():
    if not session.get('user_email'):
        flash("Please login first", "error")
        return redirect('/login')

    if session.get('role') != 'manufacturer':
        flash("Unauthorized access", "error")
        return redirect('/login')

    return render_template("manufacturer/manufacturer_home.html")

@manufacturer.route('/manufacturer/hash')
def manufacturer_hash():
    if not session.get('user_email'):
        flash("Please login first", "error")
        return redirect('/login')

    if session.get('role') != 'manufacturer':
        flash("Unauthorized access", "error")
        return redirect('/login')

    return render_template("manufacturer/manufacturer_hash.html")

@manufacturer.route('/save-proof-json', methods=['POST'])
def save_proof_json():
    if not session.get('user_email'):
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.get_json()

    output_folder = os.path.join(current_app.root_path, "static", "generated")
    os.makedirs(output_folder, exist_ok=True)

    filename = "proofData.json"
    file_path = os.path.join(output_folder, filename)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    return jsonify({
        "success": True,
        "message": "JSON saved successfully",
        "file_url": f"/static/generated/{filename}"
    })


@manufacturer.route('/mark-sent', methods=['POST'])
def mark_sent():
    item_id = request.json.get("itemId")

    #conn = sqlite3.connect(DATABASE)
    conn = sqlite3.connect(current_app.config['DATABASE'])
    cur = conn.cursor()

    cur.execute("UPDATE products SET sent = 1 WHERE itemId = ?", (item_id,))
    conn.commit()
    conn.close()

    return {"success": True}