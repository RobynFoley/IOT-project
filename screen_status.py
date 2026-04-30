from flask import Flask, request

app = Flask(__name__)

@app.route("/phone")
def phone():
    state = request.args.get("state")
    print("Phone state:", state)

    if state == "UNLOCKED":
        print("🚨 TRIGGER ALARM")

    return "OK"

app.run(host="0.0.0.0", port=5000)
