from flask import Flask, jsonify
from flask_cors import CORS
import os

# Import Blueprints
from routes.user import users_bp
from routes.medicine import medicines_bp
from routes.doctors import doctors_bp
# If you have appointments, uncomment below
# from routes.appointment import appointments_blueprint

def create_app():
    app = Flask(__name__)

    # Enable CORS (needed for frontend like Vercel)
    CORS(app)

    # Register Blueprints
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(medicines_bp, url_prefix='/medicines')
    app.register_blueprint(doctors_bp, url_prefix='/doctors')
    
    # Optional: appointments
    # app.register_blueprint(appointments_blueprint, url_prefix='/appointments')

    # Health check route (IMPORTANT for deployment)
    @app.route('/')
    def home():
        return jsonify({
            "status": "success",
            "message": "Backend is running 🚀"
        })

    return app


# Create app instance for gunicorn
app = create_app()





if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)