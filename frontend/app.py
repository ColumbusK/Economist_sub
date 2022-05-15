from init import app
from flask import session, render_template, g, request

@app.route('/')
@app.route('/sub')
def index():
    return render_template("index.html")

@app.route('/add_email', methods=['post'])
def add_email():
    return request.form["email"]

if __name__ == "__main__":
    app.run(debug=True)