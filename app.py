from flask import Flask, request, render_template, redirect, url_for, session
import secrets
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
chat_history = []
socketio = SocketIO(app)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("data")
        if username:
            session["username"] = username
            return redirect(url_for("chatpage"))
    return render_template("aju.html")

@app.route("/chatpage", methods=["GET", "POST"])
def chatpage():
    if "username" not in session:
        return redirect(url_for("home"))
    messages = chat_history
    username = session["username"]
    socketio.emit('{username} has joined this place!')
    return render_template("chatpage.html", messages=messages, username=username)

@app.route("/logout")
def logout():
    session.pop("username", None)
    print("log out")
    return redirect(url_for("home"))
@socketio.on('message')
def handle_message(message):
    chat_history.append(message)
    send(message, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)
