import logging
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Utiliser votre propre URI de base de données
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Configurer le logging
logging.basicConfig(filename='sql_injection_attempts.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

# Exemple de modèle utilisateur
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Liste des motifs d'injection SQL courants
SQL_INJECTION_PATTERNS = [
    r"(\%27)|(\')|(\-\-)|(\%23)|(#)",
    r"(\%22)|(\")|(\%3D)|(=)|(\%3B)|(;)",
    r"\b(SELECT|UPDATE|DELETE|INSERT|UNION|DROP|ALTER|CREATE|TRUNCATE|EXEC)\b",
    r"(\%28)|(\()|(\%29)|(\))",
]

def is_sql_injection(query):
    for pattern in SQL_INJECTION_PATTERNS:
        if re.search(pattern, query, re.IGNORECASE):
            return True
    return False

@app.before_request
def sql_injection_protection():
    for key, value in request.args.items():
        if is_sql_injection(value):
            logging.info(f"SQL Injection attempt detected: {key}={value}")
            abort(403)

@app.route('/')
def home():
    return "Welcome to the SQL Injection Protected Site!"

@app.route('/search')
def search():
    query = request.args.get('query')
    if query and not is_sql_injection(query):
        # Utiliser des requêtes paramétrées pour éviter les injections SQL
        results = User.query.filter(User.username.like(f"%{query}%")).all()
        return f"Search results for: {', '.join([user.username for user in results])}"
    else:
        abort(403)

def main():
    db.create_all()  # Crée les tables de la base de données
    app.run(debug=True)

if __name__ == "__main__":
    main()
