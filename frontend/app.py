from re import T
from init import app
from flask import session, render_template, g


@app.route('/')
def index():
    return render_template("index.html")



app.run(debug=True)