from flask import Flask, request, abort
import re

app = Flask(__name__)

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
            print(f"SQL Injection attempt detected: {key}={value}")
            abort(403)

@app.route('/')
def home():
    return "Welcome to the SQL Injection Protected Site!"

@app.route('/search')
def search():
    query = request.args.get('query')
    # Assurez-vous d'utiliser des requêtes paramétrées avec votre base de données
    return f"Search results for: {query}"

if __name__ == "__main__":
    app.run(debug=True)
