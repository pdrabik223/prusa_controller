from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/send_gcode")
def send_gcode():
    gcode_str = request.json.get("gcode", "")
    


if __name__ == "__main__":
    app.run(debug=True)