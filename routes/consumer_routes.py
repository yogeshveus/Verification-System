from flask import Blueprint, render_template, session, redirect, flash, get_flashed_messages

consumer = Blueprint('consumer', __name__)

@consumer.route('/consumer')
def consumer_dashboard():
    if 'user_email' not in session:
        flash("Please login first", "error")
        return redirect('/login')

    if session.get('role') != 'consumer':
        flash("Not a Consumer, unauthorized access", "error")
        return redirect('/manufacturer')

    return render_template("consumer.html")