from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)


@app.route('/')
def home_page():
    login_failed = 0
    return render_template("index.html", login_failed=login_failed)


@app.route('/login_to_dashboard', methods = ['GET', 'POST'])
def authenticate_key():
    secret_key = b"\xb1;\xf4\xa7\xb8\x12\x84\xe1\xd5G\xcec\xa5\x8c\xee\\\x12G\xd9\xf0\xeaa\xe2\x06\xf9\xcf?\xf4\xd8\xc5K:"
    input_key = request.form.get("auth_key")
    hash_input = hashlib.pbkdf2_hmac('sha256', bytes('password', 'utf-8'), bytes(input_key, 'utf-8'), 100042)
    
    if hash_input == secret_key:
        return render_template("dashboard.html")
    else:
        login_failed = 1
        return render_template("index.html", login_failed=login_failed)


@app.route('/annotate_mcomps')
def base_annotation():
    return


if __name__ == "__main__":
    app.run()