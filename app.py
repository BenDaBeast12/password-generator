
from flask import Flask, request
import random
import string

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    password = ""

    if request.method == "POST":
        strength = request.form["strength"]
        length = max(5, min(10, int(request.form["length"])))

        if strength == "easy":
            characters = string.ascii_lowercase
        elif strength == "medium":
            characters = string.ascii_letters + string.digits
        else:
            characters = string.ascii_letters + string.digits + "!@#$%"

        password = "".join(random.choice(characters) for _ in range(length))

    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Password Generator</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="container">
            <h1>Password Generator</h1>
            <form method="post">
                <label for="strength">Password strength</label>
                <select name="strength" id="strength">
                    <option value="easy">Easy</option>
                    <option value="medium">Medium</option>
                    <option value="hard">Hard</option>
                </select>

                <label for="length">Password length (5–10)</label>
                <input type="number" name="length" id="length"
                       min="5" max="10" value="8" required>

                <button type="submit">Generate Password</button>
            </form>
            <h2>Password: """ + password + """</h2>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
