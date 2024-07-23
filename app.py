from flask import Flask, jsonify, render_template, redirect, url_for, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/location')
def location():
    return render_template('location.html')

@app.route('/run_2012_update', methods=['POST'])
def run_2012_update():
    data = request.json
    units = data.get('units')
    save_units_to_file(units)
    result = run_script('resource_allocation.py', units)
    if result['status'] == 'success':
        return jsonify({'status': 'success', 'redirect_url': url_for('result')})
    else:
        return jsonify({'status': 'error', 'output': result['output']})

@app.route('/run_live_update', methods=['POST'])
def run_live_update():
    data = request.json
    units = data.get('units')
    save_units_to_file(units)
    result = run_script('live.py', units)
    if result['status'] == 'success':
        return jsonify({'status': 'success', 'redirect_url': url_for('result')})
    else:
        return jsonify({'status': 'error', 'output': result['output']})

def run_script(script_name, units):
    import subprocess
    try:
        result = subprocess.run(['python', script_name, str(units)], capture_output=True, text=True)
        if result.returncode == 0:
            return {'status': 'success', 'output': result.stdout}
        else:
            return {'status': 'error', 'output': result.stderr}
    except Exception as e:
        return {'status': 'error', 'output': str(e)}

def save_units_to_file(units):
    try:
        with open('total_units.txt', 'w') as file:
            file.write(str(units))
    except Exception as e:
        print(f"Error saving units to file: {e}")

@app.route('/result')
def result():
    file_path = 'results.txt'
    
    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
        status = 'success'
    except Exception as e:
        file_contents = str(e)
        status = 'error'
    
    return render_template('result.html', status=status, result=file_contents)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

if __name__ == '__main__':
    app.run(debug=True)