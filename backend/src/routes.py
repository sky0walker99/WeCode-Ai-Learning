from flask import Flask


@app.route('/')
def custom():
    return "<h2>  THIs is testing  <h2>"

