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
    try:
        # Read the file
        with open('results.txt', 'r') as file:
            content = file.read()
        
        # Split the content by the delimiter
        entries = content.split('--------------------')

        results = []
        for entry in entries:
            lines = [line.strip() for line in entry.split('\n') if line.strip()]
            if len(lines) < 4:
                # Skip incomplete or malformed entries
                continue

            # Extract the details
            location = lines[0].split(': ')[1].strip()
            units_allocated = lines[1].split(': ')[1].strip()
            current_rainfall = lines[2].split(': ')[1].strip()
            elevation = lines[3].split(': ')[1].strip()

            results.append({
                'location': location,
                'units_allocated': units_allocated,
                'current_rainfall': current_rainfall,
                'elevation': elevation
            })
        
        if results:
            return render_template('result.html', status='success', result=results)
        else:
            return render_template('result.html', status='failure', result='No valid data found.')

    except Exception as e:
        return render_template('result.html', status='failure', result=f'An error occurred: {str(e)}')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

if __name__ == '__main__':
    app.run(debug=True)