from flask import Flask 

app = Flask(__name__)

@app.route('/')
def signin_page():
    return "Hello! Welcome to the annotation interface!"

if __name__ == "__main__":
    app.run()