from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/admit')
def admit():
    return render_template('admit.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/main')
def mainpage():
    return render_template('mainpage.html')

@app.route('/trip')
def trip():
    return render_template('trip.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/budget')
def budget():
    return render_template('budget.html')

if __name__=='__main__':
    app.run(debug="True")