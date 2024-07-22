from flask import Flask, render_template, redirect, url_for, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/location')
def location():
    return render_template('location.html')

@app.route('/run_2012_update')
def run_2012_update():
    try:
        result = subprocess.run(['python', 'resource_allocation.py'], check=True, text=True, capture_output=True)
        return jsonify({'status': 'success', 'output': result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'output': e.stderr})

@app.route('/run_live_update')
def run_live_update():
    try:
        result = subprocess.run(['python', 'live.py'], check=True, text=True, capture_output=True)
        return jsonify({'status': 'success', 'output': result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'output': e.stderr})

if __name__ == '__main__':
    app.run(debug=True)
