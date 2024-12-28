import os
import secrets
from flask import Flask, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO, send
from werkzeug.utils import secure_filename

# Flask App Setup
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
socketio = SocketIO(app)

# File Upload Configuration
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Data Storage
user_profiles = {}
chat_history = []

# Routes
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("data")
        profile_pic = request.files.get("profilePic")

        if username:
            session["username"] = username

            if profile_pic:
                filename = secure_filename(profile_pic.filename)
                profile_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                profile_pic.save(profile_path)
                user_profiles[username] = filename
            else:
                user_profiles[username] = "default.png"  # Set default profile picture

            return redirect(url_for("chatpage"))

    return render_template("aju.html")

@app.route("/chatpage", methods=["GET"])
def chatpage():
    if "username" not in session:
        return redirect(url_for("home"))

    username = session["username"]
    profile_pic = user_profiles.get(username, "default.png")  # Use default if not set
    return render_template("chatpage.html", username=username, profile_pic=profile_pic)


@app.route("/logout")

def logout():
    username = session.pop("username", None)
    profile_pic_system = user_profiles.get("System", "system.png")
    if username:
         socketio.emit('message', {
            "username": "Server",
            "message": f"{username} has left the chat!",
            "profilePic": url_for('static', filename=f"uploads/{profile_pic_system}"),
        })
    return redirect(url_for("home"))
@socketio.on('message')
def handle_message(message):
    username = session.get("username")
    if username:
        profile_pic = user_profiles.get(username, "default.png")  # Use default if not set
        profile_pic_url = url_for('static', filename=f"uploads/{profile_pic}")

        message_data = {
            "username": username,
            "message": message,
            "profilePic": profile_pic_url
        }

        chat_history.append(message_data)
        send(message_data, broadcast=True)
if __name__ == "__main__":
    socketio.run(app, debug=True)
