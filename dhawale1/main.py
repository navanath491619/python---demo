from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_navatah():
    return "im navanath"
if __name__ == "__main__":
    app.run()