from flask import Blueprint, request, render_template, session, redirect, flash, get_flashed_messages
from services.auth_service import register_user, login_user
from services.auth_service import get_user_by_email

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")  

    data = request.form
    print("FORM DATA:", data)

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not all([name, email, password, role]):
        flash("All fields are required", "error")
        return redirect('/register')
    
    existing_user = get_user_by_email(email)  

    if existing_user:
        flash("User already exists", "error")
        return redirect('/register')
    register_user(name, email, password, role)
    flash("Registration successful!", "success")
    return redirect('/login')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")  

    data = request.form

    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        flash("All fields are required", "error")
        return redirect('/login')

    result = login_user(email, password)  

    if not result["status"]:
        flash("Invalid email or password", "error")
        return redirect('/login')

    user = get_user_by_email(email)
    session['user_email'] = email
    session['role'] = user['role']
    session['name'] = user['name']

    if user['role'] == 'manufacturer':
        flash("Login successful!", "success")
        return redirect('/manufacturer')
    else:
        flash("Login successful!", "success")
        return redirect('/consumer')
    
@auth.route('/logout')
def logout():
    session.clear()
    flash("Successfully logged out!", "success")   
    return redirect('/login')  