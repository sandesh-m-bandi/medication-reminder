from flask import Flask, jsonify, request
from flask_cors import CORS
import os

# Import Blueprints
from routes.user import users_bp
from routes.medicine import medicines_bp
from routes.doctors import doctors_bp


def create_app():
    app = Flask(__name__)

    # Enable CORS
    CORS(app)

    # Register Blueprints
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(medicines_bp, url_prefix='/medicines')
    app.register_blueprint(doctors_bp, url_prefix='/doctors')

    # -------------------------------
    # Home Route
    # -------------------------------
    @app.route('/')
    def home():
        return jsonify({
            "status": "success",
            "message": "Backend is running 🚀"
        })

    # -------------------------------
    # Login Route
    # -------------------------------
    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if email == "test@gmail.com" and password == "1234":
            return jsonify({
                "success": True,
                "user": {"email": email}
            })
        else:
            return jsonify({
                "success": False,
                "message": "Invalid credentials"
            })

    # -------------------------------
    # Reminders Route
    # -------------------------------
    @app.route("/reminders/all", methods=["GET"])
    def get_reminders():
        reminders = [
            {"status": "taken"},
            {"status": "missed"},
            {"status": "pending"}
        ]
        return jsonify(reminders)

    return app


# Create app instance
app = create_app()


# Run locally / Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)