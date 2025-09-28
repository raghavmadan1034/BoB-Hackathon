from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy

# Initialize app and extensions
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secure secret
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and JWT Manager
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Initialize Limiter with only app and key_func argument
limiter = Limiter(get_remote_address, app=app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Route for login and JWT generation
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)


    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        access_token = create_access_token(identity=username, additional_claims={"role": user.role})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid credentials"}), 401

# Secured route with JWT and Role-based access control
@app.route('/banking_data', methods=['GET'])
@limiter.limit("5 per minute")  # Rate limit: 5 requests per minute
@jwt_required()
def get_banking_data():
    current_user = get_jwt_identity()
    claims = get_jwt()  # Updated: Get JWT claims using get_jwt()

    # Check role-based access control
    if claims['role'] == 'Admin':
        return jsonify(data="Sensitive banking data here"), 200
    elif claims['role'] == 'User':
        return jsonify(data="Non-sensitive banking data here"), 200
    else:
        return jsonify({"msg": "You are not authorized to access this data"}), 403

# Rate-limited API Example
@app.route('/transaction_history', methods=['GET'])
@limiter.limit("2 per minute")
@jwt_required()
def get_transaction_history():
    return jsonify(data="User's transaction history"), 200

if __name__ == '__main__':
    app.run(debug=True)

