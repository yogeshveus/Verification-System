from flask import Blueprint, request, render_template, session, redirect
from services.product_service import get_product_types, save_product, add_product_type, get_all_products

manufacturer = Blueprint('manufacturer', __name__)

@manufacturer.route('/add-product-type', methods=['POST'])
def add_product():

    from flask import request, redirect, session

    if not session.get('user_email'):
        return redirect('/login')

    if session.get('role') != 'manufacturer':
        return "Unauthorized", 403

    new_product = request.form.get('newProduct')

    if not new_product:
        return "Invalid input", 400

    add_product_type(new_product, session.get('user_email'))

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
        return "Unauthorized", 403

    data = request.form
    if request.method == 'POST':
        itemId = data.get('itemId')
        product_type_id = data.get('productDropdown')
        metadataHash = data.get('metadataHash')

        if not email:
            return "User not logged in", 401

        if not all([itemId, product_type_id, metadataHash]):
            return "Missing fields", 400

        save_product(itemId, product_type_id, metadataHash, email)
        return redirect('/manufacturer')

    return render_template(
        "manufacturer.html",
        products=products,
        stored_products=stored_products
    )

