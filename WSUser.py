from flask import Flask, jsonify, request, render_template, redirect, url_for
import hashlib

app = Flask(__name__)

# Dati simulati
users = [
    {
        "id": 1,
        "name": "Mario Rossi",
        "email": "mario.rossi@example.com",
        "password": hashlib.md5("password1".encode()).hexdigest(),
        "roles": ["admin", "editor"],
        "active": True
    },
    {
        "id": 2,
        "name": "Luigi Verdi",
        "email": "luigi.verdi@example.com",
        "password": hashlib.md5("password2".encode()).hexdigest(),
        "roles": ["viewer"],
        "active": False
    },
    {
        "id": 3,
        "name": "Anna Bianchi",
        "email": "anna.bianchi@example.com",
        "password": hashlib.md5("password3".encode()).hexdigest(),
        "roles": ["editor"],
        "active": True
    }
]

@app.route("/api/users", methods=["GET"])
def get_users():
    return jsonify({"status": "success", "data": users})

@app.route("/api/users", methods=["POST"])
def add_user():
    if request.form:
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        if not name or not email or not password:
            return jsonify({"status": "error", "message": "Invalid data"}), 400

        hashed_password = hashlib.md5(password.encode()).hexdigest()

        new_user = {
            "id": max(user["id"] for user in users) + 1,
            "name": name,
            "email": email,
            "password": hashed_password,
            "roles": ["viewer"],
            "active": True
        }
        users.append(new_user)
        return jsonify({"status": "success", "data": new_user}), 201

    return jsonify({"status": "error", "message": "Invalid request"}), 400

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        if name and email and password:
            hashed_password = hashlib.md5(password.encode()).hexdigest()
            new_user = {
                "id": max(user["id"] for user in users) + 1,
                "name": name,
                "email": email,
                "password": hashed_password,
                "roles": ["viewer"],
                "active": True
            }
            users.append(new_user)
            return "<h1>Registrazione completata!</h1><a href='/register'>Torna al modulo</a>", 201
        else:
            return "<h1>Errore: tutti i campi sono obbligatori.</h1><a href='/register'>Torna al modulo</a>", 400

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Registrazione</title>
    </head>
    <body>
        <h1>Registrazione Nuovo Utente</h1>
        <form action="/register" method="POST">
            <label for="name">Nome:</label><br>
            <input type="text" id="name" name="name" required><br>
            <label for="email">Email:</label><br>
            <input type="email" id="email" name="email" required><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password" required><br><br>
            <button type="submit">Registrati</button>
        </form>
    </body>
    </html>
    '''

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        user = next((u for u in users if u["email"] == email and u["password"] == hashed_password), None)
        if user:
            return redirect(url_for("update_user_form", user_id=user["id"]))
        else:
            return "<h1>Credenziali non valide</h1><a href='/login'>Riprova</a>", 401

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
    </head>
    <body>
        <h1>Login</h1>
        <form action="/login" method="POST">
            <label for="email">Email:</label><br>
            <input type="email" id="email" name="email" required><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password" required><br><br>
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    '''

@app.route("/update/<int:user_id>", methods=["GET", "POST"])
def update_user_form(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return "<h1>Utente non trovato</h1><a href='/login'>Torna al login</a>", 404

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        if name:
            user["name"] = name
        if email:
            user["email"] = email
        if password:
            user["password"] = hashlib.md5(password.encode()).hexdigest()
        return "<h1>Dati aggiornati con successo</h1><a href='/login'>Logout</a>", 200

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Aggiorna Utente</title>
    </head>
    <body>
        <h1>Aggiorna i tuoi dati</h1>
        <form action="/update/{user_id}" method="POST">
            <label for="name">Nome:</label><br>
            <input type="text" id="name" name="name" value="{user['name']}" required><br>
            <label for="email">Email:</label><br>
            <input type="email" id="email" name="email" value="{user['email']}" required><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password" required><br><br>
            <button type="submit">Aggiorna</button>
        </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
