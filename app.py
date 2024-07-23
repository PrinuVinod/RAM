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
    # Read the result file
    with open('results.txt', 'r') as file:
        result_data = file.read().strip().split('\n--------------------\n')
        result_entries = []
        for entry in result_data:
            lines = entry.split('\n')
            result_entries.append({
                'location': lines[0].split(': ')[1],
                'units_allocated': lines[1].split(': ')[1],
                'current_rainfall': lines[2].split(': ')[1],
                'elevation': lines[3].split(': ')[1]
            })
    
    # Read the total units file
    with open('total_units.txt', 'r') as file:
        total_units = file.read().strip()
    
    # Read the units left file
    with open('units_left.txt', 'r') as file:
        units_left = file.read().strip()
    
    # Check the status
    status = 'success' if result_entries else 'failed'
    
    return render_template('result.html', result=result_entries, total_units=total_units, units_left=units_left, status=status)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

if __name__ == '__main__':
    app.run(debug=True)