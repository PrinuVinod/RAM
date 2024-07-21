from flask import Flask, render_template, request, redirect, url_for
import subprocess
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'run_report' in request.form:
            return redirect(url_for('units_input'))

    return render_template('index.html')

@app.route('/units', methods=['GET', 'POST'])
def units_input():
    if request.method == 'POST':
        total_units_available = request.form['units']
        with open('total_units.txt', 'w') as f:
            f.write(total_units_available)

        subprocess.run(['python', 'resource_allocation.py'])

        return redirect(url_for('results'))

    return render_template('units_input.html')

@app.route('/results')
def results():
    try:
        with open('results.txt', 'r') as f:
            results = f.read()
    except FileNotFoundError:
        results = "No results available."

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
