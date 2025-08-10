# main_app.py
from flask import Flask, render_template, redirect, url_for
import subprocess
import sys
import os

# --- Flask App Setup ---
# We tell Flask where to find the 'templates' folder.
app = Flask(__name__, template_folder='templates')

@app.route('/')
def dashboard():
    """Serves the main dashboard page."""
    return render_template('Dashboard.html')

@app.route('/run_blueprint_generator')
def run_blueprint_script():
    """
    This route executes the modelum_gui.py script in a new process.
    """
    print("Received request to run Blueprint Generator GUI...")
    try:
        # Use Popen to run the script in a new process without blocking the server.
        # sys.executable ensures the script runs with the same Python interpreter.
        subprocess.Popen([sys.executable, 'modelum_gui.py'])
    except FileNotFoundError:
        print("ERROR: 'modelum_gui.py' not found. Make sure it's in the same directory as main_app.py.")
    
    # Instantly redirect the user back to the dashboard.
    return redirect(url_for('dashboard'))

@app.route('/run_budget_estimator')
def run_budget_script():
    """
    This route executes the budget_gui.py script in a new process.
    """
    print("Received request to run Budget Estimator GUI...")
    try:
        subprocess.Popen([sys.executable, 'budget_gui.py'])
    except FileNotFoundError:
        print("ERROR: 'budget_gui.py' not found. Make sure it's in the same directory as main_app.py.")
        
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    # use_reloader=False is important for preventing issues when using subprocess
    print("Starting Modelum Dashboard Server...")
    print("Open your web browser and go to http://127.0.0.1:5000")
    app.run(debug=True, port=5000, use_reloader=False)
