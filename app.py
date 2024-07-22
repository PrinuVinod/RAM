from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/location')
def location():
    return render_template('location.html')

@app.route('/run_2012_update')
def run_2012_update():
    # Add your logic here to run the 2012 update
    # For example, you can call a function to execute the update
    # Your function to run the 2012 update goes here
    return redirect(url_for('location'))

@app.route('/run_live_update')
def run_live_update():
    # Add your logic here to run the live update
    # For example, you can call a function to execute the update
    # Your function to run the live update goes here
    return redirect(url_for('location'))

if __name__ == '__main__':
    app.run(debug=True)
