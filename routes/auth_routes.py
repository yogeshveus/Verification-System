from flask import Blueprint, request, render_template, session, redirect
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
        return "Missing fields", 400
    
    existing_user = get_user_by_email(email)  

    if existing_user:
        return "User already exists", 409  
    register_user(name, email, password, role)
    return f"User {name} registered successfully"


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")  

    data = request.form
    print("FORM DATA:", data)

    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return "Missing fields", 400
    login_user(email, password)

    user = get_user_by_email(email)
    session['user_email'] = email
    session['role'] = user['role']


    if user['role'] == 'manufacturer':
        return redirect('/manufacturer')
    
@auth.route('/logout')
def logout():
    session.clear()       
    return redirect('/login')  