import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'a-very-secret-key-that-you-should-change'

# Dummy data for kid users as requested
KID_USERS = {
    'kid6@example.com': {'password': 'password6', 'age': 6, 'name': 'Rohan'},
    'kid11@example.com': {'password': 'password11', 'age': 11, 'name': 'Tanya'},
    'kid16@example.com': {'password': 'password16', 'age': 16, 'name': 'Arjun'}
}

# --- Main Routes ---

@app.route('/')
def index():
    """Serves the main home page."""
    return render_template('index.html')

@app.route('/login-choice')
def login_choice():
    """Serves the new page to choose between Parent and Student login."""
    return render_template('choice.html')

@app.route('/parent-login', methods=['GET', 'POST'])
def parent_login():
    """Handles the parent login logic."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Dummy credentials as requested
        if email == 'parent@example.com' and password == 'password':
            session['logged_in'] = True
            session['user_type'] = 'parent'
            return redirect(url_for('parent_dashboard'))
        else:
            flash('Invalid credentials. Please try again.')
            return redirect(url_for('parent_login'))

    return render_template('parent_login.html')

@app.route('/parent-dashboard')
def parent_dashboard():
    """Shows the parent dashboard if the user is logged in."""
    if not session.get('logged_in') or session.get('user_type') != 'parent':
        flash('Please log in as a parent to view the dashboard.')
        return redirect(url_for('parent_login'))
    return render_template('parent_dashboard.html')

@app.route('/kid-login', methods=['GET', 'POST'])
def kid_login():
    """Handles the student login with dummy credentials and redirects based on age."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = KID_USERS.get(email)
        
        if user and user['password'] == password:
            session['logged_in'] = True
            session['user_type'] = 'kid'
            session['user_info'] = user
            
            age = user['age']
            if age <= 9:
                return redirect(url_for('chillar_party'))
            elif age <= 14:
                return redirect(url_for('smart_spenders'))
            else:
                return redirect(url_for('wealth_builders'))
        else:
            flash('Invalid credentials. Please try again.')
            return redirect(url_for('kid_login'))
            
    return render_template('kid_login.html')

# --- Age-Specific App Routes ---
@app.route('/chillar-party')
def chillar_party():
    """Serves the 'Chillar Party' page for kids aged 4-9."""
    if session.get('user_type') != 'kid':
        return redirect(url_for('kid_login'))
    return render_template('chillar_party.html', user=session.get('user_info'))

@app.route('/smart-spenders')
def smart_spenders():
    """Serves the 'Smart Spenders' page for kids aged 10-14."""
    if session.get('user_type') != 'kid':
        return redirect(url_for('kid_login'))
    return render_template('smart_spenders.html', user=session.get('user_info'))

@app.route('/wealth-builders')
def wealth_builders():
    """Serves the 'Wealth Builders' page for teens aged 15-18."""
    if session.get('user_type') != 'kid':
        return redirect(url_for('kid_login'))
    return render_template('wealth_builders.html', user=session.get('user_info'))


# --- Placeholder routes from your original files for completeness ---

@app.route('/parent-register')
def parent_register():
    return render_template('parent_register.html')

@app.route('/kids-app')
def kids_app():
    return render_template('kids_app.html')

@app.route('/logout')
def logout():
    """Logs the user out."""
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)